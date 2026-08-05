// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.20;

/**
 * @title GovernmentTenderSystem UsersManager
 * @dev Инкапсулирует логику работы с информацией о компаниях
 */
contract GTS_Users
{
    // Компания в системе
    struct User
    {
        address id;

        string title;
        string description;

        string cities;
        string telephones;
        string emails;
    }

    mapping(address => User) users;

    // Только зарегистрированные пользователи
    modifier registeredOnly()
    {
        require(users[msg.sender].id != address(0), "You are not registered in the system");
        _;
    }

    // Пользователь зарегистрирован
    event UserRegistered
    (
        address indexed id,
        string title
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
        require(users[msg.sender].id == address(0), "You are registered in the system");

        // Создаем новую компанию по переданным данным
        users[msg.sender] = User({
            id: msg.sender,
            title: _title,
            description: _description,
            cities: _cities,
            telephones: _telephones,
            emails: _emails
        });

        emit UserRegistered(msg.sender, _title);
    }
}