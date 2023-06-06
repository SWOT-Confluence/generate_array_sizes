# generate array size

Generate Array Size is a Lambda function that returns the array size for the following levels of input data:
- basin
- reach
- HiVDI sets
- MetroMan sets
- Sic4dVar sets

The Lambda function accesses the input EFS to load appropriate JSON data and tracks the length of the lists contained within. It sends this data back to the `confluence-workflow` Step Function.