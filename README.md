## OBOS Damallsvenskan 2019 predictions

These are the notes for a small ML project that I'm doing with my daughter [Eowyn](https://github.com/paronglass), 12 years old.

**Usage:**

`python3 scrape.py <filename>` produces a CSV file called `<filename>` (_obos-da-2019.csv_) that contains all of the results so far.

`python3 gen_features.py <input> <output>` reads the CSV file `<input>` (_obos-da-2019.csv_) and calculates and adds new columns to it and saves it in `<output>` (_obos-da-2019-fe.csv_).

`python3 transform.py <input> <output>` reads the CSV file `<input>` (_obos-da-2019-fe.csv_) and prepares it for use by a classifier. It stores the result in `<output>` (_train.csv_).

The above steps should be chained together so that the output of one is the input to the next. The final output can then be used to predict match results with

`python3 RFClassifier.py <input>` which produces a hundred different RandomForestClassifiers by training on the data in `<input>` (_train.csv_) and has them predict the outcome and finally produce a single estimate by averaging the predictions.

See the [wiki](https://github.com/loss-fn/obos-damallsvenskan-2019/wiki) for more information.