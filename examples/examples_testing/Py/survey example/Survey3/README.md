## Survey System
###### Joe Halcisak - SE310 - Spring 2023


### Serialization
The following directories and file names are used by the serialization functionality of this project.
  * Surveys
    * Surveys are named using this convention: `{surveyName}.survey`
    * Surveys are saved in the `outputs/surveys` directory.
  * Tests
    * Tests are named using this convention: `{testName}.test`
    * Tests are saved in the `outputs/tests` directory.
  * Responses to Surveys & Tests
    * Responses are saved in the `outputs/responses/{surveyOrTestName}` directory, in the main root of the project.
    * Responses are named using this convention: `{surveyOrTestName}-resp-{numberOfResponse}.response`

### Testing Purposes
  * There is an example test and an example survey located in the appropriate directories mentioned above.
  * You can load them using the options after running `Main`