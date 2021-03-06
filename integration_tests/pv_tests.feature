Feature: PV Tests

  Scenario: PV limits the minimum selling rate
     Given we have a scenario named strategy_tests/pv_final_selling_rate
     And d3a is installed
     When we run the d3a simulation with strategy_tests.pv_final_selling_rate [24, 60, 60]
     Then the storages buy energy for no more than the min PV selling rate

  Scenario: PV CONSTANT based price decrease
     Given we have a scenario named strategy_tests/pv_const_price_decrease
     And d3a is installed
     When we run the d3a simulation with strategy_tests.pv_const_price_decrease [24, 60, 60]
     Then the PV strategy decrease its sold/unsold offers price as expected

  Scenario: UserProfile PV follows the profile provided by the user as dict
     Given we have a scenario named strategy_tests/user_profile_pv_dict
     And d3a is installed
     When we run the d3a simulation with strategy_tests.user_profile_pv_dict [24, 60, 60]
     Then the UserProfile PV follows the PV profile as dict

  Scenario: Predefined PV follows the profile provided by the user as csv
     Given we have a scenario named strategy_tests/user_profile_pv_csv
     And d3a is installed
     When we run the d3a simulation with strategy_tests.user_profile_pv_csv [24, 60, 60]
     Then the UserProfile PV follows the PV profile of csv

  Scenario: Predefined PV follows the profile provided by the user
     Given we have a scenario named strategy_tests/predefined_pv_test
     And d3a is installed
     When we run the d3a simulation with strategy_tests.predefined_pv_test [24, 60, 60]
     Then the predefined PV follows the PV profile

  Scenario: Predefined PV follows the csv profile provided by the user
     Given a PV profile csv as input to predefined PV
     And the scenario includes a predefined PV
     When the simulation is running
     Then the predefined PV follows the PV profile from the csv

  Scenario: Custom PV strategy works as expected
    Given we have a scenario named jira/d3asim_640_custom_pv
    When we run the d3a simulation with jira.d3asim_640_custom_pv [24, 60, 60]
    Then the PV offers energy as expected at an expected price

  Scenario: PV max_panel_power_W argument changes power of a single PV panel
     Given we have a scenario named strategy_tests/pv_max_panel_output
     And d3a is installed
     When we run the d3a simulation with strategy_tests.pv_max_panel_output [24, 60, 60]
     Then the load buys at most the energy equivalent of 200 W

  Scenario: PV global setting max_panel_power_W changes power of all PV panels
     Given we have a scenario named strategy_tests/pv_max_panel_power_global
     And d3a is installed
     When we run the d3a simulation with strategy_tests.pv_max_panel_power_global [24, 60, 60]
     Then the load buys at most the energy equivalent of 400 W