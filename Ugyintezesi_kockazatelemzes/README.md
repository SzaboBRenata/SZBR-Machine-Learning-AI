AI-Based Analysis and Risk Classification of Administrative Cases

1. Project Overview

	Project title: AI-Based Analysis and Risk Classification of Administrative Cases

	Programming language: Python
	Development environment: PyCharm
	Machine learning approach: Supervised machine learning
	Algorithm: Logistic Regression
	Main libraries: Pandas, Scikit-learn, Matplotlib, Joblib, OpenPyXL

	Project objective

	The objective of this project is to develop a machine learning application that analyses administrative case data and estimates the probability of a case exceeding its administrative deadline.

	The application uses historical case characteristics to identify potential delays and assigns each new case to one of three risk categories:

	LOW risk
	MEDIUM risk
	HIGH risk

	The purpose is to demonstrate how artificial intelligence and data analysis can support administrative processes, improve workload monitoring, and help identify cases that may require additional attention.

	The project currently represents a working prototype using artificially generated data.

2. Project Structure

	The project is organised into Python scripts, input data, a trained model, and output files.

			Ugyintezesi_kockazatelemzes/
			│
			├── data/
			│   ├── ugyek_adatok.xlsx
			│   └── uj_ugyek.xlsx
			│
			├── eredmenyek/
			│   ├── ugytipusok.png
			│   ├── kesedelmek.png
			│   ├── hianypotlasok.png
			│   ├── roc_gorbe.png
			│   ├── modell_eredmenyek.xlsx
			│   └── uj_ugyek_kockazati_eredmenye.xlsx
			│
			├── generate_data.py
			├── analyze_data.py
			├── train_model.py
			├── predict.py
			├── predict2.py
			└── ugy_kockazati_modell.pkl

	The files have separate responsibilities. This makes the application easier to understand, maintain, test, and extend.

3. Development Process – Chronological Order

	Step 1 – Generating the training dataset

	Python file: generate_data.py

		The first step was to create a synthetic administrative dataset containing 1,000 cases.

		The dataset includes the following variables:

		Variable 							Description

		Ugy_azonosito						Unique case identifier

		Ugytipus							Type of administrative case

		Beerkezes_modja						Electronic or paper submission

		Hianypotlasok_szama					Number of requests for missing information

		Ugyintezesi_napok					Number of administrative processing days

		Hataridoig_hatralevo_napok			Days remaining until the deadline

		Ugyfelmegkeresesek_szama			Number of customer enquiries

		Dokumentum_hianyos					Whether the documentation is incomplete

		Korabbi_hasonlo_ugy_kesett			Whether a similar previous case was delayed

		Hatarido_tullepes					Whether the administrative deadline was exceeded
		
		Five administrative case categories were included:

			Press registration (Sajtó)

			Advertising (Reklám)

			Infrastructure route cases (Nyomvonal)

			Frequency-related cases (Frekvencia)

			Market surveillance (Piacfelügyelet)

		The target variable was Hatarido_tullepes, indicating whether a case exceeded its deadline.

		Result: A training dataset containing 1,000 records was successfully generated and saved as an Excel file.

		ugyek_adatok.xlsx

	Step 2 – Exploratory data analysis

	Python file: analyze_data.py

		The next step was to examine the generated dataset and identify basic patterns and distributions.

		The analysis included:

			Distribution of administrative case types.

			Number and distribution of delayed cases.

			Frequency of missing-document requests.

			Basic statistical summaries.

		Three visualisations were generated:

			ugytipusok.png – Distribution of administrative case types.

			kesedelmek.png – Distribution of delayed and non-delayed cases.

			hianypotlasok.png – Distribution of requests for missing information.

		Result: The dataset was successfully analysed, and the charts were saved in the results directory.

	Step 3 – Training the machine learning model

	Python file: train_model.py

		A supervised machine learning model was developed using Logistic Regression.

		The target variable was converted into numerical values:

			No delay = 0

			Delay = 1

		The dataset was divided into two parts:

			Training dataset: 80% (800 records)

			Testing dataset: 20% (200 records)

		The model used numerical and categorical input variables.

		Numerical variables were processed using StandardScaler, while categorical variables were transformed using OneHotEncoder.

		The preprocessing steps and the Logistic Regression classifier were combined into a single Scikit-learn pipeline.

		The model was trained using the Adam-independent standard Logistic Regression optimisation implemented by Scikit-learn, with balanced class weights to account for the unequal distribution of delayed and non-delayed cases.

		The following evaluation measures were calculated:

			Accuracy

			Precision

			Recall

			F1-score

			ROC-AUC

		A confusion matrix and ROC curve were also generated.

		Result: The model was successfully trained and evaluated.

		The ROC-AUC value was 1.00 on the generated test dataset.

		The trained pipeline was saved as:

			ugy_kockazati_modell.pkl

		The model evaluation results were saved in:

			eredmenyek/modell_eredmenyek.xlsx

		The ROC curve was saved as:

			eredmenyek/roc_gorbe.png

	Step 4 – Saving and reusing the trained model

		After training, the model was saved using Joblib.

		This is important because the model does not need to be trained again every time a new administrative case is analysed.

		The saved .pkl file contains the complete machine learning pipeline, including the preprocessing operations and the trained classifier.

		The application can load this file and use it to make predictions on new data.

	Step 5 – Preparing new administrative cases

		A separate Excel file was created for testing the trained model with new administrative cases.

		Input file: data/uj_ugyek.xlsx

		The file contains 20 new cases.

		The new records include the same input variables required by the trained model, such as:

			Case type

			Submission method

			Number of missing-document requests

			Processing time

			Number of customer enquiries

			Incomplete documentation

			Previous delays in similar cases

		The target variable Hatarido_tullepes is not included because the model must predict this outcome.

		The new cases are independent input records, and the model does not require their actual delay status in advance.

	Step 6 – Predicting the risk of administrative delays

	Python file: predict.py – Original prediction script

		The initial version of the prediction program, developed to apply the trained machine learning model to new administrative cases.

	Python file: predict2.py – Extended prediction script

		The improved version of the prediction program. It loads new cases from an Excel file, calculates the probability of deadline overruns, assigns risk categories (LOW, MEDIUM, HIGH), and exports the results to Excel.

		This script loads the previously trained model and reads the 20 new administrative cases from the Excel file.

		For each case, the model calculates the estimated probability of exceeding the administrative deadline.

		The probability is then converted into a risk category using the following thresholds:

			Estimated probability		Risk category

			Below 40%					LOW

			40% to below 70%			MEDIUM

			70% or above				HIGH

		These thresholds are illustrative business rules selected for the prototype. They are not automatically learned by the machine learning algorithm.

		The script then adds two columns to the input data:

			Keses_valoszinusege_%

			Kockazati_besorolas

		The results are exported into a new Excel file.

	Step 7 – Generating and reviewing the results

	Output file: eredmenyek/uj_ugyek_kockazati_eredmenye.xlsx

		The application successfully processed all 20 new administrative cases.

		The output file contains the original case information together with the estimated delay probability and the assigned risk category.

		The complete process, from reading the input Excel file to generating the final risk classification, was successfully executed.

4. Results of the 20 New Cases

	The model generated the following risk distribution:

		Risk category		Number of cases		Percentage

		LOW								18			 90%

		MEDIUM							 0			  0%

		HIGH							 2			 10%

		Total							20			100%

	High-risk cases

	Two cases received a HIGH risk classification.

		Case ID 	Case type			Missing-document requests	Processing days		Estimated delay probability

		UGY0105		Market surveillance				 8					41						96.85%

		UGY0108		Advertising						12					16						98.14%

	Both cases were also marked as having incomplete documentation.

	The model assigned these cases a high estimated probability of exceeding their administrative deadlines.

	Examples of low-risk cases

	The remaining 18 cases received LOW risk classifications.

	For example:

		UGY0101: estimated delay probability of 0.03%.

		UGY0113: estimated delay probability of 0.09%.

		UGY0118: estimated delay probability of 0.19%.

	No cases were classified as MEDIUM risk.

	Important: These probabilities are predictions produced by a model trained on synthetic data. They should not be interpreted as validated real-world probabilities or as proof that a particular administrative case will be delayed.

5. Summary of Completed Work

	The following seven development stages have been completed:

		1. Synthetic data generation: Created a dataset containing 1,000 administrative cases.

		2. Data analysis: Examined the data and generated statistical charts.

		3. Machine learning development: Built and trained a Logistic Regression classification model.

		4. Model evaluation: Calculated evaluation metrics, generated a confusion matrix and ROC curve, and saved the results.

		5. Model persistence: Saved the complete trained pipeline in a .pkl file.

		6. New case preparation: Created an Excel dataset containing 20 new administrative cases.

		7. Automated prediction: Developed a Python script that reads new cases, calculates delay probabilities, assigns risk categories, and exports the results to Excel.

	The project demonstrates an end-to-end machine learning workflow, from data preparation and model training to automated predictions on new records.

6. Future Development – Three Main Directions

	The current version is a functional prototype. Three important development areas have been identified.

	1. Improving the realism and quality of the training data

		The current training dataset is artificially generated, and the delayed cases have been assigned deliberately distinguishable characteristics.

		This may explain the unusually high ROC-AUC result of 1.00.

		The next development stage should include:

			Creating more realistic synthetic data.

			Introducing natural variation and uncertainty into the dataset.

			Avoiding overly obvious relationships between input variables and the target.

			Using real historical administrative data where access and data protection requirements permit.

			Ensuring that the model does not receive information that would not be available at the time of prediction.

		The objective is to build a model that can identify meaningful patterns rather than simply recognise artificial rules in the training data.

	2. Explaining why a case receives a high-risk classification

		The current application provides a probability and a risk category, but it does not yet explain which factors contributed most to the prediction.

		A future version could provide additional explanations, such as:

			A high number of missing-document requests.

			Incomplete documentation.

			A long processing period.

			A high number of customer enquiries.

			Previous delays in similar cases.

		Techniques such as feature importance analysis or SHAP could be investigated to make the model's predictions easier to understand.

		The objective is to create a more transparent decision-support system.

	3. Validating the model with independent data

		The model should be tested on additional administrative cases whose actual deadline outcomes are already known.

		This would allow a comparison between predicted and actual results.

		The validation process should include:

			Testing on independent historical records.

			Comparing predicted and actual delays.

			Measuring precision, recall, F1-score and ROC-AUC.

			Reviewing false positive and false negative predictions.

			Adjusting risk thresholds according to operational requirements.

		The objective is to establish whether the model can provide useful and reliable support in real administrative workflows.

7. Conclusion

	This project demonstrates the practical application of Python, data analysis, and machine learning in administrative case management.

	A complete prototype was developed, including synthetic data generation, exploratory analysis, model training, model evaluation, and automated risk classification of new administrative cases.

	The application successfully processed 20 new cases and generated an Excel report containing estimated delay probabilities and risk categories.

	The project provides a foundation for further development towards an AI-supported administrative monitoring system.

	Its potential practical value lies in identifying cases that may require attention before an administrative deadline is exceeded.

	The next major challenge is to improve the quality of the training data, make the predictions explainable, and validate the model using independent real-world data.
