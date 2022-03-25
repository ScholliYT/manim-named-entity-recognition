#!/bin/bash
if [ -d ./PG-NER ]; then rm -r ./PG-NER; fi
rm -r PG-NER
manedit --project_name PG-NER \
    --quick_present_export ./media/videos/slides/720p30/sections/NamedEntityRecognition1_1.json \
    --quick_present_export ./media/videos/slides/720p30/sections/Problem1_2.json \
    --quick_present_export ./media/videos/slides/720p30/sections/Motivation1_3.json \
    --quick_present_export ./media/videos/slides/720p30/sections/OldWorkingPrinciple2_1.json \
    --quick_present_export ./media/videos/slides/720p30/sections/NewWorkingPrinciple2_2.json \
    --quick_present_export ./media/videos/slides/720p30/sections/AscendingIndexWordEmbedding2_3.json \
    --quick_present_export ./media/videos/slides/720p30/sections/OneHotWordEmbedding2_4.json \
    --quick_present_export ./media/videos/slides/720p30/sections/OneHotWordEmbeddingPlot2_5.json \
    --quick_present_export ./media/videos/slides/720p30/sections/WordEmbedding2_6.json \
    --quick_present_export ./media/videos/slides/720p30/sections/ChallengesWithHistoricalData4_1.json
