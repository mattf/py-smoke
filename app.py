from flask import Flask, render_template

from pyspark.sql import SparkSession
from pyspark.ml.feature import Word2Vec


jabberwocky = """'Twas brillig, and the slithy toves
Did gyre and gimble in the wabe;
All mimsy were the borogoves,
And the mome raths outgrabe.

'Beware the Jabberwock, my son!
The jaws that bite, the claws that catch!
Beware the Jubjub bird, and shun
The frumious Bandersnatch!'

He took his vorpal sword in hand:
Long time the manxome foe he sought -
So rested he by the Tumtum tree,
And stood awhile in thought.

And as in uffish thought he stood,
The Jabberwock, with eyes of flame,
Came whiffling through the tulgey wood,
And burbled as it came!

One, two! One, two! And through and through
The vorpal blade went snicker-snack!
He left it dead, and with its head
He went galumphing back.

'And has thou slain the Jabberwock?
Come to my arms, my beamish boy!
O frabjous day! Callooh! Callay!
He chortled in his joy.

'Twas brillig, and the slithy toves
Did gyre and gimble in the wabe;
All mimsy were the borogoves,
And the mome raths outgrabe."""

app = Flask(__name__)

data = map(lambda x: (x.split(),), jabberwocky.translate(None, "';,.!:-?").lower().split('\n'))

spark = SparkSession.builder.appName('py-smoke').getOrCreate()
documentDF = spark.createDataFrame(data, ["text"])
word2Vec = Word2Vec(vectorSize=3, seed=41, minCount=0, inputCol="text", outputCol="result")
model = word2Vec.fit(documentDF)

target = 'jabberwock'
result = model.findSynonyms(target, 1).first().word

@app.route("/")
def root():
    return render_template('index.html',
                           target=target,
                           result=result)

app.run(host='0.0.0.0', port=8080)
