# Created by john at 28/08/2018
Feature: Request Taxi
  # Request and get a taxi.

  Scenario: Request Taxi
    Given Taxi system is running
    When A rider hails a taxi
    Then A taxi arrives
