# 'Given' Should be : a swedish speaking user. However this doesn't work.
Feature: take-note
  Scenario Outline: Take note in Swedish
    Given an english speaking user 
      When the user says "<Swedish prompt with note>"
      Then "fastnotes-skill" should reply with dialog from "note.taken.dialog"

  Examples: Swedish prompts with notes
        | Swedish prompt with note                       |
        | kan du skriva ner att det här är en anteckning |
        | skriv ner att det här är en anteckning         |
        | anteckna att det här är en anteckning          |
        | skriv ned det här är en anteckning             |
        | anteckning det här är en anteckning            |

  # Scenario Outline: Take note in English
  #   Given an english speaking user
  #     When the user says "<English prompt with note>"
  #     Then "fastnotes-skill" should reply with dialog from "note.taken.dialog"

  # Examples: English promps with notes
  #       | English prompt with note                          |
  #       | could you please take a note that this is a note  |
  #       | could you please take a note this is a note       |
  #       | could you please jot down that this is a note     |
  #       | please jot that this is a note                    |
  #       | could you take a note that this is a note         |
  #       | note this is a note                               |