# -*- coding: utf-8 -*-
import json
from tafsir_tools import get_selected_tafsir, get_tafsir_from_tebyan

verse_id = 1
sura_id = 1
AyehID = 1
besmellah = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"
with open('translate_dataset.txt', 'a') as g:
    with open('quran.csv', 'r') as f:
        f.readline()
        for i in range(2875):
            f.readline()
        AyehID = 2876
        for line in f:
            _, sura_id, verse_id, aye = line.strip().split(',')
            sura_id = int(sura_id)
            print("AyehID : %d and sura_id : %d" % (AyehID, sura_id))
            verse_id = int(verse_id)
            aye = aye.replace("\"", "").strip()
            if sura_id > 1 and verse_id == 1:
                aye = aye.replace(besmellah, '').strip()
            j = json.loads(get_tafsir_from_tebyan(AyehID))
            try:
                html = j['d']['Text'].replace(
                    '<b>', '**Aye**').replace('</b>', '**/Aye**')
            except Exception as e:
                with open('not_translate.txt', 'a') as f:
                    f.write(str(sura_id) + ',' + str(verse_id) + '\n')
            else:
                selected_tafsir = get_selected_tafsir(html, aye)
                g.write(selected_tafsir + '|' + aye)
                g.write('\n')
            AyehID += 1
