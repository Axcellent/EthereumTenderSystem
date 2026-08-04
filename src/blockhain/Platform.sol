// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.20;

/**
 * @title GovernmentTenderSystem
 * @dev Децентрализованная платформа для государственных закупок с автоматическим выбором поставщика
 */
contract GovernmentTenderSystem
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
        uint256 reputation;         // Репутация для авторанжирования

        uint256 price;              // Предложенная цена
        uint256 deadline;           // Предлагаемый срок    

        bool isActive;              // Актуален ли отклик
    }

    // Статус контракта
    enum ContractStatus 
    {
        Pending,
        Executing,
        Completed,
        Failed,
        Judging
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

        string description;       // Краткое описание (удалю потом)        

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



    address public government;

    // Репутация участников
    mapping(address => uint256) public reputation;

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
    mapping(uint256 => uint256[]) public contractReviews; // все отзывы по контракту

    

    modifier onlyGovernment()
    {
        require(msg.sender == government, "Only government can do this");
        _;
    }

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

    modifier contractExists(uint256 _contractId)
    {
        require(_contractId > 0 && _contractId <= contractCounter, "Contract does not exist");
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

        address winner,
        uint256 amount
    );

    event ReportSubmitted
    (
        uint256 indexed reportId,

        // чтобы искать все отчеты по контракту
        uint256 indexed contractId,

        uint256 proofCid
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

    event PaymentReleased
    (
        uint256 indexed contractId,

        address winner,
        uint256 amount
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


    

    // ---------- Конструктор ----------

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
    ) external
    {
        // check tender
        require(_deadline > block.timestamp, "Deadline must be in future");
        require(_biddingDeadline > block.timestamp, "Bidding deadline must be in future");
        require(_budget > 0, "Budget must be positive");

        // check parent tender (если субподряд)
        if (_parentTenderId > 0)
        {
            require(_parentTenderId < tenderCounter, "Tender does not exist");
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
    ) external tenderExists(_tenderId) onlyTenderCreator(_tenderId)
    {
        require(tenders[_tenderId].status != TenderStatus.Executing, "This tender is already in work or denied");
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
    ) external tenderExists(_tenderId)
    {
        Tender storage tender = tenders[_tenderId];

        // check tender
        require(tender.status == TenderStatus.Opened, "Tender is not open for bidding");
        require(block.timestamp <= tender.biddingDeadline, "Bidding period has ended");

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
            reputation: reputation[msg.sender],
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
    ) external
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
    ) public tenderExists(_tenderId) onlyTenderCreator(_tenderId)
    {
        Tender storage tender = tenders[_tenderId];
        require(tender.status == TenderStatus.Closed, "Tender has to be in closed-bidding status");                

        uint256 bestBidId = 0;
        uint256 bestScore = 0;
        for (uint i = 0; i < tenderBids[_tenderId].length; i++)
        {
            uint256 bidId = tenderBids[_tenderId][i];

            Bid storage bid = bids[bidId];
            if (!bid.isActive)
                continue;

            uint256 rep = reputation[bid.bidder];
            // TODO: correct formula            
            uint256 score = (rep * 1e18) / bid.price;
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
        emit ContractCreated(contractCounter, _tenderId, winner, price);
    }

    /**
     * @dev Эскроу
     * * Должно быть вызвано после выбора победителя.
     */
    function financeContract
    (
        uint256 _tenderId
    ) external payable tenderExists(_tenderId) onlyTenderCreator(_tenderId)
    {
        Contract storage contractData = contracts[tenderContract[_tenderId]];
        require(contractData.status == ContractStatus.Pending, "Contract is not in pending status");        
        require(msg.value == contractData.amount, "Amount must match contract amount");

        contractData.status = ContractStatus.Executing;        
        tenders[contractData.tenderId].status = TenderStatus.Executing;
    }

   

    function getTenderBids(uint256 _tenderId) external view returns (uint256[] memory)
    {
        return tenderBids[_tenderId];
    }

    function getContractReports(uint256 _contractId) external view returns (uint256[] memory)
    {
        return contractReports[_contractId];
    }

    function getContractReviews(uint256 _contractId) external view returns (uint256[] memory)
    {
        return contractReviews[_contractId];
    }

    function getReputation(address _addr) external view returns (uint256)
    {
        return reputation[_addr];
    }
}