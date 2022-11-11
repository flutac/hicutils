From ImmuneDB Link
------------------

For a hosted ImmuneDB instance, you can directly download and load data
from the website link. Depending on the database size, initially
gathering the data may take some time. After it is downloaded, the
cached version will be used unless the data is explicitly deleted.

.. code:: ipython3

    import hicutils.core.io as io
    
    df = io.pull_immunedb_data(
        'https://myurl.com/immunedb',
        'mydb',
        'example_data_immunedb'
    )
    
    # Show a snippet of the resulting DataFrame
    df[['clone_id', 'subject', 'v_gene', 'j_gene', 'cdr3_aa', 'copies', 'shm']]




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>clone_id</th>
          <th>subject</th>
          <th>v_gene</th>
          <th>j_gene</th>
          <th>cdr3_aa</th>
          <th>copies</th>
          <th>shm</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>8248</th>
          <td>6311533</td>
          <td>HPAP015</td>
          <td>IGHV2-5</td>
          <td>IGHJ4</td>
          <td>CAHSWVRYNSGWGFHYW</td>
          <td>34</td>
          <td>1.14</td>
        </tr>
        <tr>
          <th>9810</th>
          <td>6326493</td>
          <td>HPAP015</td>
          <td>IGHV2-70|2-70D</td>
          <td>IGHJ4</td>
          <td>CARPHGSSGWYYFDYW</td>
          <td>31</td>
          <td>4.34</td>
        </tr>
        <tr>
          <th>8697</th>
          <td>6315829</td>
          <td>HPAP015</td>
          <td>IGHV2-5</td>
          <td>IGHJ4</td>
          <td>CARGQWLAPNHFDYW</td>
          <td>27</td>
          <td>4.56</td>
        </tr>
        <tr>
          <th>7970</th>
          <td>6308963</td>
          <td>HPAP015</td>
          <td>IGHV2-5</td>
          <td>IGHJ4</td>
          <td>CAHRGSSWDYW</td>
          <td>24</td>
          <td>1.37</td>
        </tr>
        <tr>
          <th>8549</th>
          <td>6314347</td>
          <td>HPAP015</td>
          <td>IGHV2-5</td>
          <td>IGHJ4</td>
          <td>CAHSTIRFQYYFDSW</td>
          <td>22</td>
          <td>3.01</td>
        </tr>
        <tr>
          <th>...</th>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>4137</th>
          <td>7029341</td>
          <td>HPAP017</td>
          <td>IGHV1-46</td>
          <td>IGHJ3</td>
          <td>CAAVRYYDSSGYFAAGDSDYGRAGAFDIW</td>
          <td>1</td>
          <td>3.32</td>
        </tr>
        <tr>
          <th>4135</th>
          <td>7029336</td>
          <td>HPAP017</td>
          <td>IGHV1-46</td>
          <td>IGHJ3</td>
          <td>CAAANYYDXSGYYHYAFDIW</td>
          <td>1</td>
          <td>3.79</td>
        </tr>
        <tr>
          <th>4134</th>
          <td>7029309</td>
          <td>HPAP017</td>
          <td>IGHV1-46</td>
          <td>IGHJ3</td>
          <td>CARDLYDSIGYYRAXAFDIW</td>
          <td>1</td>
          <td>2.31</td>
        </tr>
        <tr>
          <th>4133</th>
          <td>7029295</td>
          <td>HPAP017</td>
          <td>IGHV1-46</td>
          <td>IGHJ3</td>
          <td>XARDKYSGSYYLSDAFDIW</td>
          <td>1</td>
          <td>0.46</td>
        </tr>
        <tr>
          <th>9999</th>
          <td>7116522</td>
          <td>HPAP017</td>
          <td>IGHV3-11</td>
          <td>IGHJ6</td>
          <td>CARAYSYGQYYYYGMDVW</td>
          <td>1</td>
          <td>6.98</td>
        </tr>
      </tbody>
    </table>
    <p>40000 rows × 7 columns</p>
    </div>



From existing files with metadata in filenames
----------------------------------------------

Alternatively, if you have existing files which were exported from
ImmuneDB (either using ``immunedb_export ... clones ...`` or via the
website), they can be imported directly. Take for example the files
below:

.. code:: bash

    %%bash
    ls example_data_meta_in_names


.. parsed-literal::

    HPAP015.T1D.pooled.tsv
    HPAP017.Control.pooled.tsv


The files can be imported with the following:

.. code:: ipython3

    import hicutils.core.io as io
    
    # Specify that the metadata in the filename is the disease status
    # If there are multiple features separated with the _AND_ string
    # per the ImmuneDB specification, the second parameter should
    # be a list of all features (e.g. for age and siease ['age', 'disease'].
    df = io.read_tsvs('example_data_meta_in_names', ['disease'])
    
    # Show a snippet of the resulting DataFrame
    df[['clone_id', 'subject', 'v_gene', 'j_gene', 'cdr3_aa', 'copies', 'shm']]




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>clone_id</th>
          <th>subject</th>
          <th>v_gene</th>
          <th>j_gene</th>
          <th>cdr3_aa</th>
          <th>copies</th>
          <th>shm</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>16548</th>
          <td>6310562</td>
          <td>HPAP015</td>
          <td>IGHV2-5</td>
          <td>IGHJ4|5</td>
          <td>CARARGAYW</td>
          <td>41</td>
          <td>4.415122</td>
        </tr>
        <tr>
          <th>16771</th>
          <td>6311533</td>
          <td>HPAP015</td>
          <td>IGHV2-5</td>
          <td>IGHJ4</td>
          <td>CAHSWVRYNSGWGFHYW</td>
          <td>34</td>
          <td>1.140000</td>
        </tr>
        <tr>
          <th>19430</th>
          <td>6326493</td>
          <td>HPAP015</td>
          <td>IGHV2-70|2-70D</td>
          <td>IGHJ4</td>
          <td>CARPHGSSGWYYFDYW</td>
          <td>31</td>
          <td>4.340000</td>
        </tr>
        <tr>
          <th>17713</th>
          <td>6315829</td>
          <td>HPAP015</td>
          <td>IGHV2-5</td>
          <td>IGHJ4</td>
          <td>CARGQWLAPNHFDYW</td>
          <td>30</td>
          <td>4.629000</td>
        </tr>
        <tr>
          <th>7648</th>
          <td>6262779</td>
          <td>HPAP015</td>
          <td>IGHV1-3</td>
          <td>IGHJ4</td>
          <td>CARAVENHFDWLSNYW</td>
          <td>30</td>
          <td>5.996667</td>
        </tr>
        <tr>
          <th>...</th>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>8487</th>
          <td>7016857</td>
          <td>HPAP017</td>
          <td>IGHV1-3</td>
          <td>IGHJ3</td>
          <td>XXRQGA*QWLVLWGGDAFDIW</td>
          <td>1</td>
          <td>3.270000</td>
        </tr>
        <tr>
          <th>8488</th>
          <td>7016859</td>
          <td>HPAP017</td>
          <td>IGHV1-3</td>
          <td>IGHJ3</td>
          <td>CARVMVGYSGYGGXYXVSGYAFDIW</td>
          <td>1</td>
          <td>2.790000</td>
        </tr>
        <tr>
          <th>8492</th>
          <td>7016881</td>
          <td>HPAP017</td>
          <td>IGHV1-3</td>
          <td>IGHJ3</td>
          <td>CARGGXRQRVANYXGSGRGAFDIW</td>
          <td>1</td>
          <td>4.190000</td>
        </tr>
        <tr>
          <th>8493</th>
          <td>7016885</td>
          <td>HPAP017</td>
          <td>IGHV1-3</td>
          <td>IGHJ3</td>
          <td>CARVSSYGWESAGPDAFDXW</td>
          <td>1</td>
          <td>4.650000</td>
        </tr>
        <tr>
          <th>19892</th>
          <td>7116522</td>
          <td>HPAP017</td>
          <td>IGHV3-11</td>
          <td>IGHJ6</td>
          <td>CARAYSYGQYYYYGMDVW</td>
          <td>1</td>
          <td>6.980000</td>
        </tr>
      </tbody>
    </table>
    <p>39513 rows × 7 columns</p>
    </div>



From existing replicate files and metadata file
-----------------------------------------------

Finally, if you have AIRR-seq files for each replicate and a metadata
file, use the following to load the data.

.. code:: bash

    %%bash
    ls example_data_immunedb


.. parsed-literal::

    HPAP015.IgH_HPAP015_rep1_200p0ng.pooled.tsv
    HPAP015.IgH_HPAP015_rep2_200p0ng.pooled.tsv
    HPAP017.IgH_HPAP017_rep1_200p0ng.pooled.tsv
    HPAP017.IgH_HPAP017_rep2_200p0ng.pooled.tsv
    metadata.tsv


.. code:: ipython3

    import hicutils.core.io as io
    
    df = io.read_directory('example_data_immunedb')
    
    # Show a snippet of the resulting DataFrame
    df[['clone_id', 'subject', 'v_gene', 'j_gene', 'cdr3_aa', 'copies', 'shm']]




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>clone_id</th>
          <th>subject</th>
          <th>v_gene</th>
          <th>j_gene</th>
          <th>cdr3_aa</th>
          <th>copies</th>
          <th>shm</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>8248</th>
          <td>6311533</td>
          <td>HPAP015</td>
          <td>IGHV2-5</td>
          <td>IGHJ4</td>
          <td>CAHSWVRYNSGWGFHYW</td>
          <td>34</td>
          <td>1.14</td>
        </tr>
        <tr>
          <th>9810</th>
          <td>6326493</td>
          <td>HPAP015</td>
          <td>IGHV2-70|2-70D</td>
          <td>IGHJ4</td>
          <td>CARPHGSSGWYYFDYW</td>
          <td>31</td>
          <td>4.34</td>
        </tr>
        <tr>
          <th>8697</th>
          <td>6315829</td>
          <td>HPAP015</td>
          <td>IGHV2-5</td>
          <td>IGHJ4</td>
          <td>CARGQWLAPNHFDYW</td>
          <td>27</td>
          <td>4.56</td>
        </tr>
        <tr>
          <th>7970</th>
          <td>6308963</td>
          <td>HPAP015</td>
          <td>IGHV2-5</td>
          <td>IGHJ4</td>
          <td>CAHRGSSWDYW</td>
          <td>24</td>
          <td>1.37</td>
        </tr>
        <tr>
          <th>8549</th>
          <td>6314347</td>
          <td>HPAP015</td>
          <td>IGHV2-5</td>
          <td>IGHJ4</td>
          <td>CAHSTIRFQYYFDSW</td>
          <td>22</td>
          <td>3.01</td>
        </tr>
        <tr>
          <th>...</th>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>4137</th>
          <td>7029341</td>
          <td>HPAP017</td>
          <td>IGHV1-46</td>
          <td>IGHJ3</td>
          <td>CAAVRYYDSSGYFAAGDSDYGRAGAFDIW</td>
          <td>1</td>
          <td>3.32</td>
        </tr>
        <tr>
          <th>4135</th>
          <td>7029336</td>
          <td>HPAP017</td>
          <td>IGHV1-46</td>
          <td>IGHJ3</td>
          <td>CAAANYYDXSGYYHYAFDIW</td>
          <td>1</td>
          <td>3.79</td>
        </tr>
        <tr>
          <th>4134</th>
          <td>7029309</td>
          <td>HPAP017</td>
          <td>IGHV1-46</td>
          <td>IGHJ3</td>
          <td>CARDLYDSIGYYRAXAFDIW</td>
          <td>1</td>
          <td>2.31</td>
        </tr>
        <tr>
          <th>4133</th>
          <td>7029295</td>
          <td>HPAP017</td>
          <td>IGHV1-46</td>
          <td>IGHJ3</td>
          <td>XARDKYSGSYYLSDAFDIW</td>
          <td>1</td>
          <td>0.46</td>
        </tr>
        <tr>
          <th>9999</th>
          <td>7116522</td>
          <td>HPAP017</td>
          <td>IGHV3-11</td>
          <td>IGHJ6</td>
          <td>CARAYSYGQYYYYGMDVW</td>
          <td>1</td>
          <td>6.98</td>
        </tr>
      </tbody>
    </table>
    <p>40000 rows × 7 columns</p>
    </div>


