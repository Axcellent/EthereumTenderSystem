// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.20;

/**
 * @title GovernmentTenderSystem UsersManager
 * @dev Инкапсулирует логику работы с информацией о компаниях
 */
contract GTS_Users
{
    address public userModerator;

    enum UserStatus
    {
        Unknown,
        Active,
        Banned,
        Deleted,
        Government
    }

    // Компания в системе
    struct User
    {
        string title;
        string description;

        string cities;
        string telephones;
        string emails;

        UserStatus status;
    }

    mapping(address => User) public users;

    // Только зарегистрированные пользователи
    modifier registeredOnly()
    {
        require(users[msg.sender].status == UserStatus.Active || 
            users[msg.sender].status == UserStatus.Government, "You are not registered in the system");
        _;
    }

    // Пользователь зарегистрирован
    event UserRegistered
    (
        address indexed id,
        string title
    );

    // Пользователь заблокирован
    event UserBanned
    (
        address indexed id,
        string reason
    );

    // Пользователь разблокирован
    event UserUnbanned
    (
        address indexed id,
        string reason
    );

    // Пользователь удален
    event UserDeleted
    (
        address indexed id,
        string reason
    );

    /**
     * @dev Регистрация компании в системе
     * @param _title        - string - Название компании
     * @param _description  - string - Описание компании
     * @param _cities       - string - Города, в которых работает компания
     * @param _telephones   - string - Телефоны компании
     * @param _emails       - string - Электронные почты компании
    */
    function register
    (
        string memory _title,
        string memory _description,
        string memory _cities,
        string memory _telephones,
        string memory _emails
    ) external 
    {
        require(users[msg.sender].status == UserStatus.Unknown, "You are registered in the system");        

        // Создаем новую компанию по переданным данным
        users[msg.sender] = User({
            title: _title,
            description: _description,
            cities: _cities,
            telephones: _telephones,
            emails: _emails,
            status: UserStatus.Active
        });

        emit UserRegistered(msg.sender, _title);
    }

    /**
     * @dev Блокировка компании в системе
     * @param _userId       - address - Идентификатор в компании
     * @param _reason       - string - Причина блокировки
    */
    function banUser
    (
        address _userId,
        string memory _reason
    ) external 
    {
        require(msg.sender == userModerator, "Permition denied");

        User storage user = users[_userId];
        require(user.status == UserStatus.Active, "User is not active");
        user.status = UserStatus.Banned;

        emit UserBanned(_userId, _reason);
    }

    /**
     * @dev Функция для разблокирования компании в системе
     * @param _userId       - address - Идентификатор в компании
     * @param _reason       - string - Причина разблокировки
    */
    function unbanUser
    (
        address _userId,
        string memory _reason
    ) external 
    {
        require(msg.sender == userModerator, "Permition denied");

        User storage user = users[_userId];
        require(user.status == UserStatus.Banned, "User is not banned");
        user.status = UserStatus.Active;

        emit UserUnbanned(_userId, _reason);
    }


    /**
     * @dev Удаление компании из системы
     * @param _userId       - address - Идентификатор в компании
     * @param _reason       - string - Причина удаления
    */
    function deleteUser
    (
        address _userId,
        string memory _reason
    ) external 
    {
        require(msg.sender == userModerator, "Permition denied");

        User storage user = users[_userId];
        require(user.status != UserStatus.Unknown && user.status != UserStatus.Deleted, "User is not in system");
        user.status = UserStatus.Deleted;

        emit UserDeleted(_userId, _reason);
    }
}