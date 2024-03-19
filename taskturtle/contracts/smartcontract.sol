// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TaskManager {
    struct Task {
        address requester;
        uint price;
        address executor;
        bool isAccepted;
        bool isCompleted;
    }

    Task[] public tasks;
    address payable escrow = payable(address(this));

    function createTask(uint _price) public payable {
        require(msg.value==_price, "Vous n'avez pas assez d'argent.");
        tasks.push(Task(msg.sender, _price, address(0), false, false));
        
    }

    function acceptTask(uint _index) public payable {
        Task storage task = tasks[_index];
        require(!task.isAccepted, "Task already accepted");
        require(task.requester!=msg.sender,"The requester cannot accept his own task.");
        task.executor = msg.sender;
        task.isAccepted=true;
    }
    
    function getEscrowBalance() public view returns (uint) {
        return escrow.balance;
    }


    function completeTask(uint _index) public {
        Task storage task = tasks[_index];
        require(task.isAccepted, "Task not accepted");
        require(!task.isCompleted, "Task already completed");
        require(task.requester == msg.sender, "Only the executor can complete the task");

        task.isCompleted = true;
        payable(task.executor).transfer(task.price);
    }

    function cancelTask(uint _index) public payable{
        Task storage task = tasks[_index];
        require(task.requester==msg.sender,"Only the requester can cancel this task.");
        
        payable(task.requester).transfer(task.price);
    }


}
