Feature: Orders API Load Test

  Background:
    * url 'http://localhost:31733'

  Scenario: Get Orders
    Given path 'orders'
    When method get
    Then status 200
