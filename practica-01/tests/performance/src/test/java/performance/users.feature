Feature: Users API Load Test

  Background:
    * url 'http://localhost:8000'

  Scenario: Health Check
    Given path 'health'
    When method get
    Then status 200
