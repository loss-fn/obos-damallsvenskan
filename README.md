## OBOS Damallsvenskan 2019 predictions

These are the notes for a small ML project that I'm doing with my daughter [Eowyn](https://github.com/paronglass), 12 years old.

**Usage:**

`python3 scrape.py <filename>` produces a CSV file called `<filename>` that contains all of the results so far.

`python3 gen_features.py <input> <output>` reads the CSV file `<input>` and calculates and adds new columns to it and saves it in `<output>`.

`python3 transform.py <input> <output>` reads the CSV file `<input>` and prepares it for use by a classifier. It stores the result in `<output>`.

The above steps should be chained together so that the output of one is the input to the next. The final output can then be used to predict match results with

`python3 RFClassifier.py <input>` which produces a hundred different RandomForestClassifiers and has them predict the outcome and finally produce a single estimate by averaging the predictions.

See the [wiki](https://github.com/loss-fn/obos-damallsvenskan-2019/wiki) for more information.