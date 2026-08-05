// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.20;

import "contracts/GTPUsersManager.sol";

/**
 * @title GovernmentTenderSystem ReentrancyGuard
 * @dev Защита от fallback-атак
 */
contract GTS_ReentrancyGuard
{
    bool private _canEnter = true;

    modifier nonReentrant()
    {
        require(_canEnter, "ReentrancyGuard: Denied");
        _canEnter = false;
        _;
        _canEnter = true;
    }
}

/**
 * @title GovernmentTenderSystem SecurityManager
 * @dev Инкапсулирует логику таймера и государства
 */
contract GTS_Security is GTS_ReentrancyGuard
{
    address public government;
    address private keeper;

    modifier onlyGovernment()
    {
        require(msg.sender == government, "Only government can do this");
        _;
    }

    function setKeeper
    (
        address _keeper
    ) external onlyGovernment
    {
        keeper = _keeper;
    }
}