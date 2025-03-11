import streamlit as st
import pandas as pd

# 質問リスト
questions = {
        "q16_10": "かかりつけ医に定期的に受診している (1:当てはまらない・2:あまり当てはまらない・3:少し当てはまる・4:当てはまる)",
        "q7_8": "どのような活動、健康行動をすると自分の健康が改善されるか十分に把握している (1:当てはまらない・2:あまり当てはまらない・3:少し当てはまる・4:当てはまる)",
        "q19_7": "公共交通機関を利用して通勤している (1:当てはまらない・2:あまり当てはまらない・3:少し当てはまる・4:当てはまる)",
        "q4_8": "精神的な充実も大事なので我慢したくない (1:当てはまらない・2:あまり当てはまらない・3:少し当てはまる・4:当てはまる)",
        "q14_5": "バランスの良い食事をしている (1:当てはまらない・2:あまり当てはまらない・3:少し当てはまる・4:当てはまる)",
        "q14_2": "アプリなどを使って運動時間や運動状況を記録している (1:当てはまらない・2:あまり当てはまらない・3:少し当てはまる・4:当てはまる)",
        "q4_14": "将来、自分が介護を受けるようには絶対になりたくない (1:当てはまらない・2:あまり当てはまらない・3:少し当てはまる・4:当てはまる)",
        "q16_1": "これまで、特定健診や定期健診の結果、特定保健指導を受けたことがある (1:当てはまらない・2:あまり当てはまらない・3:少し当てはまる・4:当てはまる)",
        "q7_5": "普段の食事、運動、睡眠が自分の健康状態に大きく影響していると思う (1:当てはまらない・2:あまり当てはまらない・3:少し当てはまる・4:当てはまる)",
        "q4_4": "仕事や家事が忙しく、時間に余裕がない (1:当てはまらない・2:あまり当てはまらない・3:少し当てはまる・4:当てはまる)",
        "q19_1": "現在、同居の家族に病気の治療をしている人がいる (1:当てはまらない・2:あまり当てはまらない・3:少し当てはまる・4:当てはまる)",
        "q3_2": "何かをしようとする時、少しでも達成できれば十分と考える方である (1:当てはまらない・2:あまり当てはまらない・3:少し当てはまる・4:当てはまる)",
        "q7_3": "自分の健康状態は遺伝や年齢のせいであると思う (1:当てはまらない・2:あまり当てはまらない・3:少し当てはまる・4:当てはまる)",
        "q4_12": "将来、自分が介護を受けるのは仕方がないと思う (1:当てはまらない・2:あまり当てはまらない・3:少し当てはまる・4:当てはまる)",
        "q4_10": "肥満やメタボリックシンドロームなどになるのではないかとかなり心配している (1:当てはまらない・2:あまり当てはまらない・3:少し当てはまる・4:当てはまる)",
        "q13_1": "将来の生活に対して、強い不安を感じている (1:当てはまらない・2:あまり当てはまらない・3:少し当てはまる・4:当てはまる)",
        "q4_24": "スポーツやトレーニングでさらに良い結果をだしていきたい (1:当てはまらない・2:あまり当てはまらない・3:少し当てはまる・4:当てはまる)",
        "q3_3": "考え込むよりもまずは動いてみる方だと思う (1:当てはまらない・2:あまり当てはまらない・3:少し当てはまる・4:当てはまる)",
        "q12": "あなたが普段お出かけになるときに、傘を持って出かけるのは降水確率が何％以上の時ですか？ (1:0％以上10%未満・2:10％以上20%未満・3:20％以上30%未満・4:30％以上40%未満・5:40％以上50%未満・6:50％以上60%未満・7:60％以上70%未満・8:70％以上80%未満・9:80％以上90%未満・10:90％以上100%未満・11:100%)",
        "q8": "健康を改善・維持するために生活習慣を改善してみようと思いますか？ (1:改善するつもりはない・2:改善するつもりである（概ね6か月以内）・3:近いうちに（概ね１か月以内）改善するつもりであり、少しずつ始めている・4:既に改善に取り組んでいる（６か月未満）・5:既に改善に取り組んでいる（６か月以上）)"
    }

# クラスター分類の条件
conditions = {
    "Cluster 1": lambda row: (
        (row['q16_10'] <= 1 and row['q7_8'] > 2 and row['q19_7'] > 3 and row['q4_8'] > 2 and row['q14_5'] > 2 and row['q14_2'] <= 1) or
        (row['q16_10'] > 2 and row['q19_7'] > 3 and row['q7_8'] <= 2 and row['q4_14'] > 3 and row['q4_4'] > 2 and row['q16_1'] <= 3) or
        (row['q16_10'] <= 1 and row['q7_8'] <= 2 and row['q7_5'] == 3 and row['q19_7'] > 3 and row['q4_14'] > 2 and row['q8'] > 1) or
        (row['q16_10'] <= 1 and row['q7_8'] <= 2 and row['q7_5'] > 3 and row['q4_14'] > 2 and (row['q8'] == 2 or row['q8'] == 3) and row['q19_7'] > 1) or
        (row['q16_10'] <= 1 and row['q7_8'] > 2 and row['q19_7'] > 3 and row['q4_8'] > 2 and row['q14_5'] <= 2 and row['q4_12'] == 2) or
        (row['q16_10'] <= 1 and row['q7_8'] > 2 and row['q19_7'] > 3 and row['q4_8'] <= 2 and row['q4_4'] > 1 and row['q13_1'] > 2) or
        (row['q16_10'] == 2 and row['q19_7'] > 3 and row['q4_8'] == 3 and (row['q8'] == 2 or row['q8'] == 3) and row['q12'] <= 4 and row['q7_5'] > 3) or
        (row['q16_10'] == 2 and row['q19_7'] > 3 and row['q4_8'] == 3 and (row['q8'] == 2 or row['q8'] == 3) and row['q12'] > 4) or
        (row['q16_10'] <= 1 and row['q7_8'] <= 2 and row['q7_5'] > 3 and row['q4_14'] > 2 and row['q8'] > 3) or
        (row['q16_10'] <= 1 and row['q7_8'] <= 2 and row['q7_5'] == 3 and (row['q19_7'] == 2 or row['q19_7'] == 3) and row['q4_4'] > 2) or
        (row['q16_10'] == 2 and row['q19_7'] > 3 and row['q4_8'] <= 2 and row['q19_1'] <= 1 and row['q4_14'] > 2) or
        (row['q16_10'] <= 1 and row['q7_8'] <= 2 and row['q7_5'] > 3 and row['q4_14'] <= 2 and row['q4_10'] > 1) or
        (row['q16_10'] == 2 and row['q19_7'] > 3 and row['q4_8'] > 3 and row['q4_4'] > 2) or
        (row['q16_10'] == 2 and row['q19_7'] <= 1 and row['q4_14'] > 3 and row['q19_1'] > 1) or
        (row['q16_10'] <= 1 and row['q7_8'] > 2 and (row['q19_7'] == 2 or row['q19_7'] == 3) and row['q4_4'] > 2)
    ),
    "Cluster 2": lambda row: (
        (row['q16_10'] > 2 and row['q19_7'] <= 1 and row['q4_14'] == 3 and row['q19_1'] > 1 and (row['q16_1'] == 2 or row['q16_1'] == 3) and row['q14_5'] > 2) or
        (row['q16_10'] == 2 and (row['q19_7'] in [2, 3]) and row['q4_8'] <= 2 and row['q3_2'] == 2 and row['q7_3'] > 2 and row['q19_1'] <= 1) or
        (row['q16_10'] == 2 and (row['q19_7'] in [2, 3]) and row['q4_8'] == 3 and row['q19_1'] <= 1 and row['q8'] > 1 and row['q7_3'] <= 2) or
        (row['q16_10'] == 2 and row['q19_7'] > 3 and row['q4_8'] == 3 and (row['q8'] in [2, 3]) and row['q12'] <= 4 and row['q7_5'] <= 3) or
        (row['q16_10'] > 2 and row['q19_7'] > 3 and row['q7_8'] <= 2 and row['q4_14'] <= 2 and row['q19_1'] <= 1) or
        (row['q16_10'] == 2 and row['q19_7'] <= 1 and row['q4_14'] == 3 and row['q7_3'] <= 2 and row['q19_1'] > 1) or
        (row['q16_10'] == 2 and (row['q19_7'] in [2, 3]) and row['q4_8'] <= 2 and row['q3_2'] == 2 and row['q7_3'] <= 2) or
        (row['q16_10'] <= 1 and row['q7_8'] > 2 and (row['q19_7'] in [2, 3]) and row['q4_4'] <= 2 and row['q4_8'] <= 2) or
        (row['q16_10'] > 2 and (row['q19_7'] in [2, 3]) and row['q19_1'] > 1 and row['q7_5'] > 3 and row['q4_10'] > 2) or
        (row['q16_10'] > 2 and (row['q19_7'] in [2, 3]) and row['q19_1'] > 1 and row['q7_5'] <= 3) or
        (row['q16_10'] == 2 and row['q19_7'] > 3 and row['q4_8'] <= 2 and row['q19_1'] > 1) or
        (row['q16_10'] == 2 and (row['q19_7'] in [2, 3]) and row['q4_8'] == 3 and row['q19_1'] > 1) or
        (row['q16_10'] == 2 and (row['q19_7'] in [2, 3]) and row['q4_8'] <= 2 and row['q3_2'] > 2) or
        (row['q16_10'] == 2 and row['q19_7'] <= 1 and row['q4_14'] <= 2 and row['q4_8'] <= 2) or
        (row['q16_10'] <= 1 and row['q7_8'] <= 2 and row['q7_5'] <= 2 and row['q4_10'] > 1)
    ),
    "Cluster 3": lambda row: (
        (row['q16_10'] > 2 and row['q19_7'] > 3 and row['q7_8'] <= 2 and row['q4_14'] > 3 and row['q4_4'] > 2 and row['q16_1'] > 3) or
        (row['q16_10'] > 2 and row['q19_7'] > 3 and row['q7_8'] <= 2 and row['q4_14'] > 3 and row['q4_4'] == 2 and row['q16_1'] > 1) or
        (row['q16_10'] > 2 and row['q19_7'] <= 1 and row['q4_14'] == 3 and row['q19_1'] > 1 and (row['q16_1'] == 2 or row['q16_1'] == 3) and row['q14_5'] <= 2) or
        (row['q16_10'] > 2 and row['q19_7'] > 3 and row['q7_8'] > 2 and row['q4_10'] == 2 and row['q7_3'] > 2 and row['q19_1'] > 1) or
        (row['q16_10'] > 2 and row['q19_7'] > 3 and row['q7_8'] <= 2 and row['q4_14'] > 3 and row['q4_4'] <= 1 and row['q4_12'] <= 1) or
        (row['q16_10'] > 2 and (row['q19_7'] in [2, 3]) and row['q19_1'] <= 1 and row['q3_2'] > 1 and row['q4_10'] > 2 and row['q4_14'] > 3) or
        (row['q16_10'] > 2 and row['q19_7'] <= 1 and row['q4_14'] > 3 and row['q14_5'] <= 2 and row['q4_10'] <= 1 and row['q13_1'] > 3) or
        (row['q16_10'] > 2 and row['q19_7'] <= 1 and row['q4_14'] == 3 and row['q19_1'] > 1 and row['q16_1'] > 3) or
        (row['q16_10'] > 2 and row['q19_7'] <= 1 and row['q4_14'] == 3 and row['q19_1'] > 1 and row['q16_1'] <= 1) or
        (row['q16_10'] > 2 and row['q19_7'] <= 1 and row['q4_14'] <= 2 and row['q4_12'] > 2 and row['q7_8'] <= 2) or
        (row['q16_10'] > 2 and row['q19_7'] > 3 and row['q7_8'] <= 2 and row['q4_14'] <= 2 and row['q19_1'] > 1) or
        (row['q16_10'] > 2 and row['q19_7'] <= 1 and row['q4_14'] > 3 and row['q14_5'] > 3 and row['q19_1'] > 1) or
        (row['q16_10'] > 2 and row['q19_7'] <= 1 and row['q4_14'] <= 2 and row['q4_12'] <= 2 and row['q19_1'] > 1) or
        (row['q16_10'] > 2 and row['q19_7'] <= 1 and row['q4_14'] > 3 and row['q14_5'] <= 2 and row['q4_10'] > 1) or
        (row['q16_10'] > 2 and row['q19_7'] <= 1 and row['q4_14'] == 3 and row['q19_1'] <= 1 and row['q7_5'] > 3) or
        (row['q16_10'] > 2 and row['q19_7'] > 3 and row['q7_8'] > 2 and row['q4_10'] > 2) or
        (row['q16_10'] > 2 and row['q19_7'] > 3 and row['q7_8'] <= 2 and row['q4_14'] == 3) or
        (row['q16_10'] > 2 and row['q19_7'] <= 1 and row['q4_14'] > 3 and row['q14_5'] == 3)
    ),
    "Cluster 4": lambda row: (
        (row['q16_10'] <= 1 and row['q7_8'] > 2 and row['q19_7'] > 3 and row['q4_8'] > 2 and row['q14_5'] > 2 and row['q14_2'] > 1) or
        (row['q16_10'] > 2 and row['q19_7'] > 3 and row['q7_8'] > 2 and row['q4_10'] <= 1 and row['q4_8'] <= 2 and row['q3_3'] > 2) or
        (row['q16_10'] > 2 and (row['q19_7'] in [2, 3]) and row['q19_1'] <= 1 and row['q3_2'] > 1 and row['q4_10'] == 2 and row['q7_3'] <= 2) or
        (row['q16_10'] <= 1 and row['q7_8'] > 2 and row['q19_7'] > 3 and row['q4_8'] <= 2 and row['q4_4'] > 1 and row['q13_1'] <= 2) or
        (row['q16_10'] <= 1 and row['q7_8'] > 2 and row['q19_7'] <= 1 and row['q4_14'] > 2 and row['q4_8'] > 2 and row['q7_5'] > 3) or
        (row['q16_10'] > 2 and row['q19_7'] <= 1 and row['q4_14'] > 3 and row['q14_5'] > 3 and row['q19_1'] <= 1) or
        (row['q16_10'] <= 1 and row['q7_8'] > 2 and row['q19_7'] > 3 and row['q4_8'] <= 2 and row['q4_4'] <= 1) or
        (row['q16_10'] > 2 and row['q19_7'] > 3 and row['q7_8'] > 2 and row['q4_10'] == 2 and row['q7_3'] <= 2) or
        (row['q16_10'] > 2 and row['q19_7'] > 3 and row['q7_8'] > 2 and row['q4_10'] <= 1 and row['q4_8'] > 2) or
        (row['q16_10'] <= 1 and row['q7_8'] > 2 and (row['q19_7'] in [2, 3]) and row['q4_4'] <= 2 and row['q4_8'] > 2) or
        (row['q16_10'] > 2 and (row['q19_7'] in [2, 3]) and row['q19_1'] > 1 and row['q7_5'] > 3 and row['q4_10'] <= 2) or
        (row['q16_10'] > 2 and (row['q19_7'] in [2, 3]) and row['q19_1'] <= 1 and row['q3_2'] > 1 and row['q4_10'] <= 1) or
        (row['q16_10'] == 2 and row['q19_7'] > 3 and row['q4_8'] > 3 and row['q4_4'] <= 2 and row['q4_10'] <= 2) or
        (row['q16_10'] == 2 and row['q19_7'] > 3 and row['q4_8'] == 3 and row['q8'] > 3 and row['q7_5'] > 3) or
        (row['q16_10'] == 2 and (row['q19_7'] in [2, 3]) and row['q4_8'] > 3)
    ),
    "Cluster 5": lambda row: (
        (row['q16_10'] > 2 and row['q19_7'] > 3 and row['q7_8'] > 2 and row['q4_10'] == 2 and row['q7_3'] > 2 and row['q19_1'] <= 1) or
        (row['q16_10'] == 2 and (row['q19_7'] in [2, 3]) and row['q4_8'] == 3 and row['q19_1'] <= 1 and row['q8'] > 1 and row['q7_3'] > 2) or
        (row['q16_10'] > 2 and (row['q19_7'] in [2, 3]) and row['q19_1'] <= 1 and row['q3_2'] > 1 and row['q4_10'] == 2 and row['q7_3'] > 2) or
        (row['q16_10'] <= 1 and row['q7_8'] > 2 and row['q19_7'] > 3 and row['q4_8'] > 2 and row['q14_5'] <= 2 and row['q4_12'] > 2) or
        (row['q16_10'] > 2 and (row['q19_7'] in [2, 3]) and row['q19_1'] <= 1 and row['q3_2'] > 1 and row['q4_10'] > 2 and row['q4_14'] <= 3) or
        (row['q16_10'] <= 1 and row['q7_8'] > 2 and row['q19_7'] <= 1 and row['q4_14'] > 2 and row['q4_8'] > 2 and row['q7_5'] <= 3) or
        (row['q16_10'] <= 1 and row['q7_8'] > 2 and row['q19_7'] <= 1 and row['q4_14'] <= 2 and row['q4_24'] > 2) or
        (row['q16_10'] > 2 and row['q19_7'] <= 1 and row['q4_14'] <= 2 and row['q4_12'] > 2 and row['q7_8'] > 2) or
        (row['q16_10'] == 2 and row['q19_7'] <= 1 and row['q4_14'] == 3 and row['q7_3'] > 2 and row['q8'] > 1) or
        (row['q16_10'] == 2 and row['q19_7'] <= 1 and row['q4_14'] == 3 and row['q7_3'] <= 2 and row['q19_1'] <= 1) or
        (row['q16_10'] == 2 and row['q19_7'] <= 1 and row['q4_14'] > 3 and row['q19_1'] <= 1 and row['q4_8'] <= 3) or
        (row['q16_10'] <= 1 and row['q7_8'] > 2 and row['q19_7'] <= 1 and row['q4_14'] > 2 and row['q4_8'] <= 2) or
        (row['q16_10'] <= 1 and row['q7_8'] <= 2 and row['q7_5'] == 3 and row['q19_7'] <= 1 and row['q4_8'] <= 2) or
        (row['q16_10'] > 2 and row['q19_7'] <= 1 and row['q4_14'] == 3 and row['q19_1'] <= 1 and row['q7_5'] <= 3) or
        (row['q16_10'] == 2 and row['q19_7'] > 3 and row['q4_8'] == 3 and row['q8'] > 3 and row['q7_5'] <= 3) or
        (row['q16_10'] == 2 and row['q19_7'] <= 1 and row['q4_14'] <= 2 and row['q4_8'] > 2)
    ),
    "Cluster 6": lambda row: (
        (row['q16_10'] == 2 and (row['q19_7'] in [2, 3]) and row['q4_8'] <= 2 and row['q3_2'] == 2 and row['q7_3'] > 2 and row['q19_1'] > 1) or
        (row['q16_10'] > 2 and row['q19_7'] > 3 and row['q7_8'] > 2 and row['q4_10'] <= 1 and row['q4_8'] <= 2 and row['q3_3'] <= 2) or
        (row['q16_10'] <= 1 and row['q7_8'] > 2 and row['q19_7'] <= 1 and row['q4_14'] <= 2 and row['q4_24'] <= 2) or
        (row['q16_10'] > 2 and row['q19_7'] <= 1 and row['q4_14'] <= 2 and row['q4_12'] <= 2 and row['q19_1'] <= 1) or
        (row['q16_10'] == 2 and row['q19_7'] > 3 and row['q4_8'] <= 2 and row['q19_1'] <= 1 and row['q4_14'] <= 2) or
        (row['q16_10'] <= 1 and row['q7_8'] <= 2 and row['q7_5'] <= 2 and row['q4_10'] <= 1 and row['q4_8'] <= 2) or
        (row['q16_10'] > 2 and (row['q19_7'] in [2, 3]) and row['q19_1'] <= 1 and row['q3_2'] <= 1) or
        (row['q16_10'] == 2 and (row['q19_7'] in [2, 3]) and row['q4_8'] <= 2 and row['q3_2'] <= 1)
    ),
    "Cluster 7": lambda row: (
        (row['q16_10'] > 2 and row['q19_7'] > 3 and row['q7_8'] <= 2 and row['q4_14'] > 3 and row['q4_4'] == 2 and row['q16_1'] <= 1) or
        (row['q16_10'] <= 1 and row['q7_8'] <= 2 and row['q7_5'] == 3 and row['q19_7'] > 3 and row['q4_14'] > 2 and row['q8'] <= 1) or
        (row['q16_10'] <= 1 and row['q7_8'] <= 2 and row['q7_5'] > 3 and row['q4_14'] > 2 and (row['q8'] == 2 or row['q8'] == 3) and row['q19_7'] <= 1) or
        (row['q16_10'] <= 1 and row['q7_8'] > 2 and row['q19_7'] > 3 and row['q4_8'] > 2 and row['q14_5'] <= 2 and row['q4_12'] <= 1) or
        (row['q16_10'] > 2 and row['q19_7'] > 3 and row['q7_8'] <= 2 and row['q4_14'] > 3 and row['q4_4'] <= 1 and row['q4_12'] > 1) or
        (row['q16_10'] > 2 and row['q19_7'] <= 1 and row['q4_14'] > 3 and row['q14_5'] <= 2 and row['q4_10'] <= 1 and row['q13_1'] <= 3) or
        (row['q16_10'] == 2 and (row['q19_7'] in [2, 3]) and row['q4_8'] == 3 and row['q19_1'] <= 1 and row['q8'] <= 1) or
        (row['q16_10'] == 2 and row['q19_7'] <= 1 and row['q4_14'] == 3 and row['q7_3'] > 2 and row['q8'] <= 1) or
        (row['q16_10'] <= 1 and row['q7_8'] <= 2 and row['q7_5'] > 3 and row['q4_14'] > 2 and row['q8'] <= 1) or
        (row['q16_10'] <= 1 and row['q7_8'] <= 2 and row['q7_5'] == 3 and (row['q19_7'] in [2, 3]) and row['q4_4'] <= 2) or
        (row['q16_10'] <= 1 and row['q7_8'] <= 2 and row['q7_5'] == 3 and row['q19_7'] > 3 and row['q4_14'] <= 2) or
        (row['q16_10'] == 2 and row['q19_7'] <= 1 and row['q4_14'] > 3 and row['q19_1'] <= 1 and row['q4_8'] > 3) or
        (row['q16_10'] <= 1 and row['q7_8'] <= 2 and row['q7_5'] == 3 and row['q19_7'] <= 1 and row['q4_8'] > 2) or
        (row['q16_10'] <= 1 and row['q7_8'] <= 2 and row['q7_5'] <= 2 and row['q4_10'] <= 1 and row['q4_8'] > 2) or
        (row['q16_10'] == 2 and row['q19_7'] > 3 and row['q4_8'] > 3 and row['q4_4'] <= 2 and row['q4_10'] > 2) or
        (row['q16_10'] <= 1 and row['q7_8'] <= 2 and row['q7_5'] > 3 and row['q4_14'] <= 2 and row['q4_10'] <= 1) or
        (row['q16_10'] == 2 and row['q19_7'] > 3 and row['q4_8'] == 3 and row['q8'] <= 1)
    )
}

# クラスターの特徴
cluster_descriptions = {
    "Cluster 1": "何とかしたいが時間がない",
    "Cluster 2": "自分のことはよくわからない",
    "Cluster 3": "病気はこりごり",
    "Cluster 4": "自己管理に自信あり",
    "Cluster 5": "今は健康、それでよし",
    "Cluster 6": "将来不安、諦めモード",
    "Cluster 7": "自分は大丈夫"
}

# Streamlit UI
st.title("クラスター分類アンケート")

# ユーザーの回答を収集
responses = {}
for key, question in questions.items():
    max_val = 4 if key not in ["q12", "q8"] else (11 if key == "q12" else 5)
    responses[key] = st.radio(question, list(range(1, max_val + 1)))

# クラスター分類関数
def classify_cluster(row):
    for cluster, condition in conditions.items():
        if condition(row):
            return cluster
    return "Other"

if st.button("クラスター分類を実行"):
    # DataFrameに変換
    data = pd.DataFrame([responses])
    data['Cluster'] = data.apply(classify_cluster, axis=1)
    
    # 結果表示
    cluster_result = data.iloc[0]['Cluster']
    st.subheader("あなたのクラスター分類結果:")
    st.write(f"**{cluster_result}**")
    
    if cluster_result in cluster_descriptions:
        st.write(cluster_descriptions[cluster_result])

