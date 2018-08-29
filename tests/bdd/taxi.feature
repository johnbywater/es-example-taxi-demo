# Created by john at 28/08/2018
Feature: Request Taxi
  Request and get a taxi.

  Scenario: Rider takes a ride
    Given taxi system is running

    When a rider requests a ride from "home" to "work"
    Then a car is booked from "home" to "work"
    And the car heads to pickup at "home" and dropoff at "work"

    When the car has arrived at the pickup position
    Then the office knows the car arrived at the pickup position
    And the rider knows the car arrived at the pickup position

    When the car has arrived at the dropoff position
    Then the office knows the car arrived at the dropoff position
    And the rider knows the car arrived at the dropoff position
