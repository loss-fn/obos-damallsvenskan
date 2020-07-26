## OBOS Damallsvenskan 2019 predictions

These are the notes for a small ML project that I'm doing with my daughter [Eowyn](https://github.com/paronglass), 12 years old.

**Usage:**

`python3 scrape.py <filename>` produces a CSV file called `<filename>` (_obos-da-2019.csv_) that contains all of the results so far.

`python3 gen_features.py <input> <output>` reads the CSV file `<input>` (_obos-da-2019.csv_) and calculates and adds new columns to it and saves it in `<output>` (_obos-da-2019-fe.csv_).

`python3 transform.py <input> <output>` reads the CSV file `<input>` (_obos-da-2019-fe.csv_) and prepares it for use by a classifier. It stores the result in `<output>` (_train.csv_).

The above steps should be chained together so that the output of one is the input to the next. The final output can then be used to predict match results with

`python3 RFClassifier.py <input>` which produces a hundred different RandomForestClassifiers by training on the data in `<input>` (_train.csv_) and has them predict the outcome and finally produce a single estimate by averaging the predictions.

See the [wiki](https://github.com/loss-fn/obos-damallsvenskan-2019/wiki) for more information.

**Evaluation**

We've spent some time discussing how good our little program is at predicting the outcomes. It's worth noting that we modelled for predicting 2 numbers, the number of goals each team would score. Implicitly those numbers also tell us the match results (win, lose or tie ) for each team but we didn't model that. Having said that we can't really calaculate it's performance based on whether it got the match result correct or not, we can really only evaluate it based on how closely it predictid the number of goals for each team.

Using a `Mean Squared Error` gives a score of `3.1` for the first, `2.8` for the second and `2.7` for the third prediction. But the first prediction has 3 rounds predicted with `2.7`, `3.7` and `2.8` as it's score if we look at MSE per round. The second prediction (with 2 rounds) managed `3.5` and `2.2`.

**Future**

Maybe we can try something with the data available on [SoccerStats](https://www.soccerstats.com/).

Several series in Europe do not have a winter break which means there are more matches that we could try predicting. Two of Swedens top players have left for CD Tacon in Spain (https://www.soccerstats.com/results.asp?league=spain7) which could be interesting to follow.

This would also give us an opportunity to sharpen up the predictions a little.
