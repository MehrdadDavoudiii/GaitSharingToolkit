AI Interpreter
==============

The AI Interpreter is the core feature of Gait Sharing, providing the ability to communicate with LLMs (currently ChatGPT) and request automated descriptions of measured gait data.

File Selection
--------------

First, the user selects which files to transfer to the LLM:

- **features.txt**: The extracted features informing deviations from normal
- **Anonymized PDF**: Additional patient information not available in the features, such as spatiotemporal parameters

The user will also be asked to provide a description of the uploaded files.

.. image:: /_static/images/ai_files.png
   :width: 100%
   :alt: AI Interpreter File Selection
   :align: center

|

Prompt Engineering
------------------

The prompts sent to ChatGPT can be engineered within the tool. There are five different prompt categories available, and prompts can be customized and saved for future use.

.. image:: /_static/images/ai_prompts.png
   :width: 100%
   :alt: Prompt Categories
   :align: center

|

.. image:: /_static/images/ai_prompts2.png
   :width: 100%
   :alt: Prompt Editor
   :align: center

|

Diagnosis Context
-----------------

The diagnosis context (e.g., cerebral palsy) should be entered in the designated box to guide the LLM in generating a description of the patient's gait. The output report will be named after the patient; however, this information remains local and **is not transmitted to OpenAI**.

API Key
-------

To access OpenAI, the user needs a personal API key. Instructions for obtaining this key are provided in a pop-up window within the application.

.. image:: /_static/images/ai_apikey.png
   :width: 100%
   :alt: API Key Instructions
   :align: center

|

.. note::
   In case of difficulty acquiring the key, please contact the author for support.

Privacy and Legal Considerations
--------------------------------

As mentioned in the application, the responsibility for legal compliance rests with the user. However, uploading **anonymized features** — not curves, which could serve as biomarkers — along with a user-provided summarized diagnosis to guide the LLM, and receiving a detailed description of the measurements and general cause-and-effect chain, represents the safest approach through this platform.
