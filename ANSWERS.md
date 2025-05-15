1) Limitations to scaling
     - Reliance solely on filenames induces poor classification results
     - No user visibility into system status, user should be involved in the system
     - No file content analysis prevents more robust classification to scale across industries
     - Single thread and non batch file processing creates a bottleneck
     - Hardcoded classifier prevents effective and efficient scaling to new industries
     - No user feedback loop to improve classifier


2) How to extend classifier with additional capabilities, technologies or features?
     - Google drive login to allow users to deploy an agent on their file store, classifying all existing files and automatically classifying any newly created files
     - Add content and metadata extraction to improve classifier
     - Embedding based classification
     - Generate confidence scores for each classification
     - Have a confidence score threshold, when score is below the threshold, have a zero-shot ML or LLM fallback
     - Enable user feedback to engage the user in the system (human-in-the-loop)
     - Industry specific/specialized layouts, templates, or keyword dictionaries to specialize classifier for certain industrys, but still retain the general model
     - Performance dashboard to give Heron visibility into how the classifier is performing
     - Add a user interface to improve usability


3) How can you ensure that the classifier is robust and reliable in a production environment?
     - Testing
         - Unit test for each component (text extraction, classification, confidence scoring)
         - Integration tests to simulate edge cases (empty files, non-english text, corrupted files) and standard test cases (PDF, DOCX, PPT, XSLX, JPG, PNG)
     - Defensive programming
         - Clear and concise error messages for unreadable files, empty files, corrupted files
         - Clear and concise status messages so user knows the live status of the system
         - Fallback methods, such as LLM zero-shot ML or filename based classifications, if OCR or content based classification falls below confidence score threshold
     - Monitoring
         - Provide metrics for Heron to review such as system throughput, failure rate, success rate, latency
         - Log events for each file parsed to provide summary statistics (file type, content extraction success or failure, prediction confidence)
     - Modularity
         - Each step in the system is decoupled
         - Makes it easier to plug in new components in the future
     - Validation
         - Specific validation datasets for each industry


4) How to deploy the classifier to make it accessible for users and other services?
     - Wrap classifier as a web service with key protection
         - Flask to expose endpoint 
     - Containerize with Docker
     - Deploy to cloud using Google Cloud Run
     - For enterprise load, use Kubernetes
     - CI/CD Pipeline
