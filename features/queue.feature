Feature: Test Command Queue


  # positive
  Scenario: text queue
    Given text (Grusha Test text 15.10.2022)
    Given with (PrintCmd) command
    Given queue
    When call
    Then wait when finish queue
    Then execute (Log) 1 time

  # negative
  Scenario: text connection exception (command is repeated 1 time)
    Given text (grusha123456)
    Given queue
    And with (PrintCmd) command
    When raise connection exception
    When call
    Then wait when finish queue
    Then execute (Log) 2 time

  # negative
  Scenario: text environment exception (command is repeated 2 time)
    Given text (Grusha Test text 18.10.2022)
    Given queue
    And with (PrintCmd) command
    When raise environment exception
    When call
    Then print output
    Then wait when finish queue
    Then execute (Log) 3 time