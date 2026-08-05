// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.20;

import "contracts/GTPUsersManager.sol";
import "contracts/GTPSecurity.sol";

/**
 * @title GovernmentTenderSystem
 * @dev Децентрализованная платформа для государственных закупок с автоматическим выбором поставщика.
 * Заказы могут создаваться государством (указанным при деплое) или частными компаниями.
 * Репутация участников изменяется по итогам выполнения контрактов.
 */
contract GovernmentTenderSystem is 
    GTS_Users,
    GTS_Security
{
    // Статус тендера
    enum TenderStatus
    { 
        Opened,             // открыт
        Closed,             // прием завершен
        Processed,          // победитель выбран
        Executing,          // выполнение заказа
        Completed,          // заказ завершен
        Denied              // заказ отменен
    }

    // Тендер на выполнение работ
    struct Tender
    {
        address creator;            // Создатель заказа

        // TODO: remove strings
        // для хранения в IPFS - uint256 cid;            

        string  title;              // Краткое описание
        string  description;        // Подробное описание со ссылками
        uint256 budget;             // Максимальная сумма в wei
        uint256 deadline;

        uint256 biddingDeadline;    // Дедлайн подачи откликов UNIX
        TenderStatus status;

        uint256 parentTenderId;     // 0 – госзаказ, иначе – основной заказ для текущего субзаказа
    }

    // Отклик на тендер
    struct Bid
    {
        uint256 tenderId;

        address bidder;             // Адрес компании-исполнителя        

        uint256 price;              // Предложенная цена
        uint256 deadline;           // Предлагаемый срок    

        bool isActive;              // Актуален ли отклик
    }

    // Статус контракта
    enum ContractStatus 
    {
        Pending,
        Executing,
        Finished,
        Completed,
        Judging,
        Failed
    }

    // Контракт, заключенный на выполнение работ
    struct Contract
    {
        uint256 tenderId;         // Идентификатор работ

        address contractor;
        address owner;

        uint256 amount;           // Сумма, заблокированная на контракте

        uint256 started;
        uint256 deadline;

        ContractStatus status;
        uint256 reportId;         // ID последнего отчёта
    }

    // Статус документа
    enum DocStatus 
    {
        Pending,                    // В обработке
        Accepted,                   // Принят действительным
        Rejected                    // Отклонен
    }

    // Отчет (о работе, или на работу, или на отчет)
    struct Report
    {
        uint256 contractId;

        address reporter;           // Либо заказчик, либо исполнитель

        string description;         // Краткое описание (удалю потом)        

        DocStatus status; 
    }

    // Отзыв на звершенные работы
    struct Review
    {
        uint256 contractId;

        address from;             // Кто писал отзыв
        address to;               // На кого писался отзыв

        int8 rating;              // Оценка

        string comment;

        DocStatus status;
    }

    // Прошение на дополнительные средства
    struct Petition
    {
        uint256 contractId;        

        uint256 amount;
        string comment;    

        DocStatus status;
    }



    // Репутация участников
    mapping(address => int256) public reputation;

    uint256 public tenderCounter;
    mapping(uint256 => Tender) public tenders;

    uint256 public bidCounter;
    mapping(uint256 => Bid) public bids;

    uint256 public contractCounter;
    mapping(uint256 => Contract) public contracts;

    uint256 public reportCounter;
    mapping(uint256 => Report) public reports;

    uint256 public reviewCounter;
    mapping(uint256 => Review) public reviews;

    mapping(uint256 => uint256[]) public tenderBids;      // все отклики на тендер
    mapping(uint256 => uint256) public tenderContract;    // ID контракта по тендеру (0 если нет)

    mapping(uint256 => uint256[]) public contractReports; // все отчёты по контракту        



    modifier onlyTenderCreator(uint256 _tenderId)
    {
        require(tenders[_tenderId].creator == msg.sender, "Only tender creator can do this");
        _;
    }

    modifier tenderExists(uint256 _tenderId)
    {
        require(_tenderId > 0 && _tenderId <= tenderCounter, "Tender does not exist");
        _;
    }



    event TenderCreated
    (
        uint256 indexed tenderId,

        // чтобы искать тендеры компании и субподряды 
        address indexed creator, 
        uint256 indexed parentTenderId,

        string description, 
        uint256 budget, 
        uint256 biddingDeadline
    );

    event BidSubmitted
    (
        uint256 indexed bidId,

        // чтобы искать отклики на тендер и отклики от участника
        uint256 indexed tenderId,
        address indexed bidder,

        uint256 price
    );

    event BidWithdrawn
    (
        uint256 indexed bidId, 
        uint256 indexed tenderId
    );

    event WinnerSelected
    (
        uint256 indexed tenderId,
        uint256 indexed bidId,

        address winner,
        uint256 price
    );

    event ContractCreated
    (
        uint256 indexed contractId,
        uint256 indexed tenderId,
        // чтобы искать субподряды
        uint256 indexed parentTenderId,

        address winner,
        uint256 amount
    );

    event ReportSubmitted
    (
        uint256 indexed reportId,

        // чтобы искать все отчеты по контракту
        uint256 indexed contractId,

        string description

        //uint256 proofCid
    );

    event ReportAccepted
    (
        uint256 indexed reportId,

        // чтобы искать все отчеты по контракту
        uint256 indexed contractId
    );

    event ReportRejected
    (
        uint256 indexed reportId,

        // чтобы искать все отчеты по контракту
        uint256 indexed contractId
    );

    event ContractFinished
    (
        uint256 indexed contractId
    );

    event PaymentReleased
    (
        uint256 indexed contractId,
        // история успешных контрактов для суда 
        address indexed owner,
        address indexed contractor,

        uint256 amount,
        uint256 timestamp
    );

    event ContractFailed
    (
        uint256 indexed contractId,
        // история судебных дел для суда 
        address indexed owner,
        address indexed contractor,

        uint256 timestamp
    );

    event ReviewSubmitted
    (
        uint256 indexed reviewId,

        // чтобы искать все отзывы по контракту
        uint256 indexed contractId,

        address from,
        address to,
        int8 rating
    );


    

    constructor(address _government)
    {
        government = _government;
    }




    /**
     * @dev Создаёт новый тендер
     * @param _description      - string    - Описание заказа
     * @param _budget           - wei       - Максимальная сумма
     * @param _deadline         - timestamp - Срок выполнения
     * @param _biddingDeadline  - timestamp - Дедлайн подачи откликов
     * @param _parentTenderId   - tenderId  - 0, если гос
     */
    function createTender
    (
        string memory _title,
        string memory _description,
        uint256 _budget,
        uint256 _deadline, 
        uint256 _biddingDeadline,
        uint256 _parentTenderId
    ) external registeredOnly
    {
        // check tender
        require(_deadline > block.timestamp, "Deadline must be in future");
        require(_biddingDeadline > block.timestamp, "Bidding deadline must be in future");
        require(_budget > 0, "Budget must be positive");

        // check parent tender (если субподряд)
        if (_parentTenderId > 0)
        {
            require(_parentTenderId > 0 && _parentTenderId <= tenderCounter, "Tender does not exist");
            require(tenders[_parentTenderId].status == TenderStatus.Executing, "Tender is not executing");
        }

        // create tender
        tenderCounter++;
        tenders[tenderCounter] = Tender({
                creator: msg.sender,
                title: _title,
                description: _description,
                budget: _budget,
                deadline: _deadline,
                biddingDeadline: _biddingDeadline,
                status: TenderStatus.Opened,
                parentTenderId: _parentTenderId
            }
        );

        emit TenderCreated(tenderCounter, msg.sender, _parentTenderId, _description, _budget, _biddingDeadline);
    }

    /**
     * @dev Отменяет тендер (only creator)
     * @param _tenderId      - tenderId    - Номер заказа
     */
    function revertTender
    (
        uint256 _tenderId
    ) external registeredOnly tenderExists(_tenderId) onlyTenderCreator(_tenderId)
    {
        require(tenders[_tenderId].status == TenderStatus.Opened, "This tender is already in work, finished or denied");
        tenders[_tenderId].status = TenderStatus.Denied;
    }


    /**
     * @dev Подача отклика на тендер компанией-исполнителем.
     * @param _tenderId         - tenderId  - номер заказа
     * @param _price            - money     - цена
     * @param _estimatedTime    - timestamp - свой дедлайн выполнения
     */
    function submitBid
    (
        uint256 _tenderId,
        uint256 _price,
        uint256 _estimatedTime
    ) external registeredOnly tenderExists(_tenderId)
    {
        Tender storage tender = tenders[_tenderId];

        // check tender
        require(tender.status == TenderStatus.Opened, "Tender is not open for bidding");
        require(block.timestamp <= tender.biddingDeadline, "Bidding period has ended");
        require(tender.creator != msg.sender, "You are creator of this tender");

        // check bid
        require(_price > 0 && _price <= tender.budget, "Price must be positive and less than tender budget");
        require(_estimatedTime > 0 && _estimatedTime <= tender.deadline, "Bad estimated time");

        // check: uniqur bid on tender from company
        for (uint i = 0; i < tenderBids[_tenderId].length; i++)
        {
            uint256 bidId = tenderBids[_tenderId][i];
            if (bids[bidId].bidder == msg.sender && bids[bidId].isActive)
            {
                revert("You have already submitted a bid for this tender");
            }
        }

        // create new bid
        bidCounter++;        
        bids[bidCounter] = Bid({
            tenderId: _tenderId,
            bidder: msg.sender,            
            price: _price,
            deadline: _estimatedTime,            
            isActive: true
        });
        // add bid to tender
        tenderBids[_tenderId].push(bidCounter);
        
        emit BidSubmitted(bidCounter, _tenderId, msg.sender, _price);
    }

    /**
     * @dev Отзыв отклика до выбора победителя.
     * @param _bidId - bidId - номер отклика
     */
    function withdrawBid
    (
        uint256 _bidId
    ) external registeredOnly
    {
        require(_bidId > 0 && _bidId <= bidCounter, "Bid does not exist");

        Bid storage bid = bids[_bidId];
        // check bid
        require(bid.bidder == msg.sender, "Only bidder can revert");
        require(bid.isActive, "Bid already inactive");  

        // check tender
        uint256 _tenderId = bid.tenderId;
        require(tenders[_tenderId].status == TenderStatus.Opened, "Cannot withdraw after bidding closed");

        bid.isActive = false;
        emit BidWithdrawn(_bidId, _tenderId);        
    }

    /**
     * @dev Открыть контракт с лучшей компанией
     * @param _tenderId - tenderId - номер заказа
     */
    function openContract
    (
        uint256 _tenderId
    ) public registeredOnly tenderExists(_tenderId) onlyTenderCreator(_tenderId)
    {
        Tender storage tender = tenders[_tenderId];
        require(tender.status == TenderStatus.Closed, "Tender has to be in closed-bidding status");                

        uint256 bestBidId = 0;
        int256 bestScore = 0;
        // TODO: добавить оптимизацию в виде priority_queue
        for (uint i = 0; i < tenderBids[_tenderId].length; i++)
        {
            uint256 bidId = tenderBids[_tenderId][i];

            Bid storage bid = bids[bidId];
            if (!bid.isActive)
                continue;

            int256 rep = reputation[bid.bidder];
            // TODO: correct formula
            int256 score = (rep * 1e18) / int256(bid.price);
            if (score > bestScore)
            {
                bestScore = score;
                bestBidId = bidId;
            }
        }

        require(bestBidId > 0, "No active bids found");
        
        tender.status = TenderStatus.Processed;
        address winner = bids[bestBidId].bidder;
        uint256 price = bids[bestBidId].price;
        contractCounter++;
        contracts[contractCounter] = Contract({
            tenderId: _tenderId,
            contractor: winner,
            owner: tenders[_tenderId].creator,
            amount: price,
            started: block.timestamp,
            deadline: bids[bestBidId].deadline,
            status: ContractStatus.Pending,
            reportId: 0
        });
        tenderContract[_tenderId] = contractCounter;

        emit WinnerSelected(_tenderId, bestBidId, winner, price);
        emit ContractCreated(contractCounter, _tenderId, tender.parentTenderId, winner, price);
    }

    /**
     * @dev Эскроу
     * * Должно быть вызвано после выбора победителя.
     */
    function financeContract
    (
        uint256 _tenderId
    ) external payable registeredOnly tenderExists(_tenderId) onlyTenderCreator(_tenderId)
    {
        Contract storage contractData = contracts[tenderContract[_tenderId]];
        require(contractData.status == ContractStatus.Pending, "Contract is not in pending status");        
        require(msg.value == contractData.amount, "Amount must match contract amount");

        contractData.status = ContractStatus.Executing;        
        tenders[contractData.tenderId].status = TenderStatus.Executing;
    }

    /**
     * @dev Отправка отчета о работе
     * @param _tenderId     - tenderId  - номер заказа
     * @param _description  - string    - текст отчета (временно, потом через ipfs)
    */
    function submitReport
    (
        uint256 _tenderId,
        string memory _description,
        bool response
    ) external registeredOnly tenderExists(_tenderId)
    {
        Tender memory t = tenders[_tenderId];
        require(t.status == TenderStatus.Executing, "Tender is not executing");
        uint256 _contractId = tenderContract[_tenderId];

        Contract storage c = contracts[_contractId];
        require(response || msg.sender == c.contractor, "You are not the perfomer of contract to create report");
        require(!response || msg.sender == c.owner, "You are not the owner of contract to create response");

        reportCounter++;
        reports[reportCounter] = Report({
            contractId: _contractId,
            reporter: msg.sender,
            description: _description,
            status: DocStatus.Pending
        });
        contractReports[_contractId].push(reportCounter);

        c.reportId = reportCounter;
        emit ReportSubmitted(reportCounter, _contractId, _description);
    }

    /**
     * @dev Выполнение принятия отчета или отказа от него (разрешение/запрет на переход работы на новый этап)
     * @param _reportId - reportId  - идентификатор рассматриваемого отчета
     * @param accepted  - bool      - принимаем или отказываемся принимать
    */
    function reviewReport
    (
        uint256 _reportId,
        bool accepted
    ) external registeredOnly
    {
        require(_reportId > 0 && _reportId <= reportCounter, "Report does not exist");
        Report storage r = reports[_reportId];

        require(msg.sender != r.reporter, accepted ? "You can not accept your report" : "You can not reject your report");
        require(r.status == DocStatus.Pending, "This report is not pending");
        Contract memory c = contracts[r.contractId];

        require(c.status == ContractStatus.Executing, "This contract has been already finished");
        require(msg.sender == c.owner || msg.sender == c.contractor, "You are not participant of this contract");        

        if (accepted)
        {
            r.status = DocStatus.Accepted;
            emit ReportAccepted(_reportId, r.contractId);
        }
        else
        {
            r.status = DocStatus.Rejected;
            emit ReportRejected(_reportId, r.contractId);
        }
    }

    /**
     * @dev Подрядчик завершает контракт
     * @param _tenderId - tenderId  - идентификатор тендера, контракт на который мы закрываем
    */
    function finishContract
    (
        uint256 _tenderId
    ) external registeredOnly tenderExists(_tenderId)
    {
        Tender memory t = tenders[_tenderId];
        require(t.status == TenderStatus.Executing, "This tender is not executing");
        uint256 _contractId = tenderContract[_tenderId];

        Contract storage c = contracts[_contractId];        
        require(c.status == ContractStatus.Executing, "This contract is not executing");
        require(msg.sender == c.contractor, "You are not contractor of this contract");
        require(c.reportId != 0, "Documentation history is empty");
        // не проверяем состояние последнего отчета, чтобы дать оперативности в 
        // бюрокартической работе, конфликты могут быть урегулированы судом

        c.status = ContractStatus.Finished;

        emit ContractFinished(_contractId);
    }

    /**
     * @dev Заказчик принимает работу
     * @param _tenderId - tenderId  - идентификатор тендера, контракт на который мы закрываем
     * @param accept    - bool      - принять/отклонить
     * @param strict    - bool      - хотим ли мы подать в суд (в случае недобросовестной работы)
    */
    function acceptFinishedContract
    (
        uint256 _tenderId,
        bool accept,
        bool strict
    ) external registeredOnly tenderExists(_tenderId) onlyTenderCreator(_tenderId) nonReentrant
    {
        Tender storage t = tenders[_tenderId];
        require(t.status == TenderStatus.Executing, "This tender is not executing");
        uint256 _contractId = tenderContract[_tenderId];

        Contract storage c = contracts[_contractId];   
        require(c.status == ContractStatus.Finished, "This contract is not finished");

        if (accept)
        {
            (bool sent, ) = payable(c.contractor).call{value: c.amount}("");

            if (sent)
            {
                c.status = ContractStatus.Completed;
                t.status = TenderStatus.Completed;

                emit PaymentReleased(_contractId, c.owner, c.contractor, c.amount, block.timestamp);
            }        
            else 
            {
                revert("Payment error");
            }
        }
        else
        {
            if (strict)
            {
                c.status = ContractStatus.Judging;
                t.status = TenderStatus.Completed;
                emit ContractFailed(_contractId, c.owner, c.contractor, block.timestamp);
            }
            else
            {
                c.status = ContractStatus.Executing;
            }
        }    
    }

    /**
     * @dev Отправить отзыв на заказчика или исполнителя
     * @param _tenderId     - tenderId  - тендер, на котором вместе работали
     * @param _contractor   - bool      - мы исполнитель
     * @param _rating       - -5..5     - оценка исполнителя или заказчика
     * @param _comment      - string    - комментарий к работе
    */
    function submitReview
    (
        uint256 _tenderId,
        bool _contractor,
        int8 _rating,
        string memory _comment
    )
    external registeredOnly tenderExists(_tenderId)
    {
        Tender memory t = tenders[_tenderId];
        require(t.status == TenderStatus.Completed, "Tender is not completed");

        uint256 _contractId = tenderContract[_tenderId];
        Contract memory c = contracts[_contractId];
        require(_contractor || msg.sender == c.owner, "You are not creator of this tender");
        require(!_contractor || msg.sender == c.contractor, "You are not performer of this tender");

        require(_rating >= -5 && _rating <= 5, "Inavalid rating delta");

        for (uint256 i = 0; i < reviewCounter; i++)
        {
            require(reviews[i].from != msg.sender || _contractId != reviews[i].contractId || 
                reviews[i].status == DocStatus.Rejected, "You have accepted on pendings reviews in this tender");
        }

        address _to = (_contractor ? c.owner : c.contractor);
        reviewCounter++;
        reviews[reviewCounter] = Review({
            contractId: _contractId,
            from: msg.sender,
            to: _to,
            rating: _rating,
            comment: _comment,
            status: DocStatus.Pending
        });

        emit ReviewSubmitted(reviewCounter, _contractId, msg.sender, _to, _rating);
    }

    /**
     * @dev Вернуть средства заказчику
     * @param _tenderId     - tenderId  - тендер, по которому возврат
     * @param toCreator     - bool      - заказчик прав
    */
    function withdrawMoney 
    (
        uint256 _tenderId,
        bool toCreator
    ) external onlyGovernment tenderExists(_tenderId) nonReentrant
    {
        Tender memory t = tenders[_tenderId];
        require(t.status == TenderStatus.Completed, "Tender is not finished");
        
        Contract memory c = contracts[tenderContract[_tenderId]];
        require(c.status == ContractStatus.Judging, "Contract is not judging");

        bool sent = false;
        if (toCreator)
        {
            (sent, ) = payable(c.owner).call{value: c.amount}("");
        }
        else
        {
            (sent, ) = payable(c.contractor).call{value: c.amount}("");
        }

        if (sent)
        {   
            c.status = ContractStatus.Failed;
        }
        else
        {
            revert("Payment error");
        }
    }

    /**
     * @dev Принять отзыв достоверным
     * @param _reviewId     - reviewId  - идентификатор отзыва
     * @param accept        - bool      - принимаем или нет
    */
    function reviewReview
    (
        uint256 _reviewId,
        bool accept
    )
    external onlyGovernment
    {        
        require(_reviewId > 0 && _reviewId <= reviewCounter, "Review does not exist");

        Review storage r = reviews[_reviewId];
        require(r.status == DocStatus.Pending, "Review is not pending");

        if (accept)
        {
            r.status = DocStatus.Accepted;
            reputation[r.to] = reputation[r.to] + r.rating;
        }
        else 
        {
            r.status = DocStatus.Rejected;
        }
    }


    function getTenderBids
    (
        uint256 _tenderId
    ) external view returns (uint256[] memory)
    {
        return tenderBids[_tenderId];
    }

    function getContractReports
    (
        uint256 _contractId
    ) external view returns (uint256[] memory)
    {
        return contractReports[_contractId];
    }

    function getReputation
    (
        address _addr
    ) external view returns (int256)
    {
        return reputation[_addr];
    }

    /**
     * @dev Функция для хранителя для закрытия оставления заявок по тендерам
     * @param _tenderId     - tenderId  - идентификатор тендера, который пора закрыть
    */
    function closeTender
    (
        uint256 _tenderId
    ) external tenderExists(_tenderId)
    {
        Tender storage t = tenders[_tenderId];
        require(t.status == TenderStatus.Opened, "Tender is not opened");
        require(block.timestamp >= t.deadline, "Time for bidding is not over");
        
        t.status = TenderStatus.Closed;
    }
}