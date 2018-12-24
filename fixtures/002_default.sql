INSERT INTO `ages` (`id`, `name`, `is_active`, `created_at`)
VALUES
	(1, '0歳', 1, '2018-03-11 15:02:23.000000'),
	(2, '1歳', 1, '2018-03-11 15:02:23.000000'),
	(3, '2歳', 1, '2018-03-11 15:02:23.000000'),
	(4, '3歳', 1, '2018-03-11 15:02:23.000000'),
	(5, '4歳', 1, '2018-03-11 15:02:23.000000'),
	(6, '延長', 1, '2018-03-11 15:02:23.000000'),
	(7, 'その他', 0, '2018-03-11 15:02:23.000000');


INSERT INTO `cities` (`id`, `name`, `is_active`, `home_url`, `created_at`)
VALUES
	(1, '東京', 1, 'http://www.metro.tokyo.jp/', '2018-03-11 15:10:30.000000'),
	(2, '横浜', 0, 'http://www.city.yokohama.lg.jp/', '2018-03-11 15:10:54.000000');


INSERT INTO `licenses` (`id`, `name`, `is_active`, `created_at`)
VALUES
	(1, '認可外', 1, '2018-03-11 15:13:06.000000'),
	(2, '認可', 1, '2018-03-11 15:13:06.000000'),
	(3, '認定', 0, '2018-03-11 15:13:06.000000'),
	(4, '認証', 1, '2018-03-11 15:13:06.000000'),
	(5, '小規模', 1, '2018-03-11 15:13:06.000000'),
	(6, '横浜', 0, '2018-03-11 15:13:06.000000'),
	(7, 'その他', 0, '2018-03-11 15:13:06.000000');


INSERT INTO `school_types` (`id`, `name`, `created_at`)
VALUES
	(1, '公立', '2017-11-20 12:35:06.820343'),
	(2, '区立', '2017-11-20 12:35:06.820343'),
	(3, '私立', '2017-11-20 12:35:06.820343'),
	(4, '公設民営', '2017-11-20 12:35:06.820343'),
	(5, 'その他', '2017-11-20 12:35:06.820343');

INSERT INTO `wards` (`id`, `city_id`, `name`, `home_url`, `nursery_info_url`, `nursery_free_num_info_url`, `nursery_free_num_info_web_page_title`, `is_active`, `latitude`, `longitude`, `created_at`, `updated_at`)
VALUES
	(1, 1, '千代田区', 'https://www.city.chiyoda.lg.jp/index.html', 'http://linkdata.org/work/rdf1s3888i', 'https://www.city.chiyoda.lg.jp/koho/kosodate/hoikuen/enjiboshu/ninka-tein.html', NULL, 0, 35.68691420, 139.73885390, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(2, 1, '中央区', 'http://www.city.chuo.lg.jp/', 'http://linkdata.org/work/rdf1s3888i', 'http://www.city.chuo.lg.jp/kosodate/hoiku/ninkahoiku/akijoho.html', NULL, 0, 35.67042530, 139.75833620, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(3, 1, '港区', 'http://www.city.minato.tokyo.jp/', 'http://linkdata.org/work/rdf1s3888i', 'http://www.city.minato.tokyo.jp/kodomo/kodomo/kodomo/hoikuen/aki.html', NULL, 0, 35.65521210, 139.73271780, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(4, 1, '新宿区', 'https://www.city.shinjuku.lg.jp/', 'http://linkdata.org/work/rdf1s3888i', 'http://www.city.shinjuku.lg.jp/kodomo/file04_07_00034.html', NULL, 0, 35.70158980, 139.67418760, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(5, 1, '文京区', 'http://www.city.bunkyo.lg.jp/', 'http://opendata-catalogue.metro.tokyo.jp/dataset/t131059d0206080001', 'http://www.city.bunkyo.lg.jp/kyoiku/kosodate/okosan/nicchu/ninka/29reigetsumoushikomi.html?revision=1#boshuunitsuite', NULL, 0, 35.71774320, 139.72736570, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(6, 1, '台東区', 'http://www.city.taito.lg.jp/', 'http://opendata-catalogue.metro.tokyo.jp/dataset/t131067d0000000003', 'http://www.city.taito.lg.jp/index/kurashi/kosodate/mokutei/hoiku_youjikyouiku/hoikutakuji/hoikuen/hoikuennyuen/getureininnzuu.html', NULL, 0, 35.71324430, 139.76846930, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(7, 1, '墨田区', 'https://www.city.sumida.lg.jp/', 'http://linkdata.org/work/rdf1s3888i', 'http://www.city.sumida.lg.jp/kosodate_kyouiku/kosodate_site/hoikuen_yochien/hoikuen/aki_zyouhou/kurituhoikuen.html', NULL, 0, 35.42380000, 139.78051610, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(8, 1, '江東区', 'https://www.city.koto.lg.jp/', 'http://linkdata.org/work/rdf1s3888i', 'http://www.city.koto.lg.jp/280308/kodomo/hoiku/ninka/5903.html', NULL, 0, 35.64338660, 139.74005370, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(9, 1, '品川区', 'http://www.city.shinagawa.tokyo.jp/', 'http://linkdata.org/work/rdf1s3888i', 'http://www.city.shinagawa.tokyo.jp/PC/kodomo/kodomo-hoyou/kodomo-hoyou-hoikuen/201811191366.html', '保育園｜品川区 【2019年4月一次】保育園・小規模保育事業等入園可能数（予定）', 1, 35.61263670, 139.71624820, '2017-11-19 11:03:22.890000', '2017-11-20 12:35:07.937685'),
	(10, 1, '目黒区', 'http://www.city.meguro.tokyo.jp/', 'http://linkdata.org/work/rdf1s3888i', 'http://www.city.meguro.tokyo.jp/kurashi/kosodate/hoikuen/akijokyo.html', NULL, 0, 35.63242580, 139.65465320, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(11, 1, '大田区', 'https://www.city.ota.tokyo.jp/', 'http://linkdata.org/work/rdf1s38881i', 'http://www.city.ota.tokyo.jp/seikatsu/kodomo/hoiku/hoikushisetsu_nyukibo/aki-joho.html', NULL, 0, 35.56709780, 139.66929530, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(12, 1, '世田谷区', 'http://www.city.setagaya.lg.jp/', 'http://linkdata.org/work/rdf1s3888i', 'http://www.city.setagaya.lg.jp/kurashi/103/129/1813/496/index.html', NULL, 0, 35.63657310, 139.59946980, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(13, 1, '渋谷区', 'https://www.city.shibuya.tokyo.jp/', 'http://linkdata.org/work/rdf1s3888i', 'https://www.city.shibuya.tokyo.jp/katei/children/ikuji/hoiku_aki.html', NULL, 0, 35.66688610, 139.67511660, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(14, 1, '中野区', 'http://www.city.tokyo-nakano.lg.jp/', 'http://linkdata.org/work/rdf1s3888i', 'http://www.city.tokyo-nakano.lg.jp/dept/244000/d001477.html', NULL, 0, 35.70613050, 139.62424190, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(15, 1, '杉並区', 'http://www.city.suginami.tokyo.jp/', 'http://linkdata.org/work/rdf1s3888i', 'http://www.city.suginami.tokyo.jp/guide/kosodate/navi/aki/1004710.html', NULL, 0, 35.69867680, 139.59140090, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(16, 1, '豊島区', 'http://www.city.toshima.lg.jp/', 'http://linkdata.org/work/rdf1s3888i', 'http://www.city.toshima.lg.jp/260/kosodate/kosodate/hoikuen/nyuen/004481.html', NULL, 0, 35.72918510, 139.69758430, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(17, 1, '北区', 'http://www.city.kita.tokyo.jp/', 'http://linkdata.org/work/rdf1s3888i', 'https://www.city.kita.tokyo.jp/k-hoiku/kosodate/hoikuen/hoikuen/moshikomi/moshikomi/index.html', NULL, 0, 35.76525950, 139.69498570, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(18, 1, '荒川区', 'http://www.city.arakawa.tokyo.jp/', 'http://linkdata.org/work/rdf1s3888i', 'https://www.city.arakawa.tokyo.jp/kosodate/hoiku_takuji/hoikuen/akijoho.html', NULL, 0, 35.73982970, 139.76453770, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(19, 1, '板橋区', 'http://www.city.itabashi.tokyo.jp/', 'http://linkdata.org/work/rdf1s3888i', 'http://www.city.itabashi.tokyo.jp/c_kurashi/036/036575.html', NULL, 0, 35.76846640, 139.63858190, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(20, 1, '練馬区', 'http://www.city.nerima.tokyo.jp/', 'http://linkdata.org/work/rdf1s3888i', 'http://www.city.nerima.tokyo.jp/kurashi/shussan/hoiku/hoikuen/nyuuen/ninka-aiki.html', NULL, 0, 35.74590310, 139.58700090, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(21, 1, '足立区', 'http://www.city.adachi.tokyo.jp/', 'http://linkdata.org/work/rdf1s3888i', 'https://www.city.adachi.tokyo.jp/kodomo-nyuuen/k-kyoiku/kosodate/hoikuen-h26boshu.html', NULL, 0, 35.77814320, 139.76220540, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(22, 1, '葛飾区', 'http://www.city.katsushika.lg.jp/', 'http://linkdata.org/work/rdf1s3888i', 'http://www.city.katsushika.lg.jp/kurashi/1000056/1002334/index.html', NULL, 0, 35.75393900, 139.81892960, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(23, 1, '江戸川区', 'https://www.city.edogawa.tokyo.jp/', 'http://linkdata.org/work/rdf1s3888i', 'https://www.city.edogawa.tokyo.jp/kosodate/kosodate/hoiku/hoikuen/h29boshu/index.html', NULL, 0, 35.69183430, 139.80647940, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(24, 2, '鶴見区', 'http://www.city.yokohama.lg.jp/tsurumi/', 'http://linkdata.org/work/rdf1s4879i', 'http://www.city.yokohama.lg.jp/kodomo/unei/nyusho-jokyo.html', NULL, 0, 35.49454760, 139.64533730, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(25, 2, '神奈川区', 'http://www.city.yokohama.lg.jp/kanagawa/', 'http://linkdata.org/work/rdf1s4879i', 'http://www.city.yokohama.lg.jp/kodomo/unei/nyusho-jokyo.html', NULL, 0, 35.48501700, 139.58347240, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(26, 2, '西区', 'http://www.city.yokohama.lg.jp/nishi/', 'http://linkdata.org/work/rdf1s4879i', 'http://www.city.yokohama.lg.jp/kodomo/unei/nyusho-jokyo.html', NULL, 0, 35.45719630, 139.60368710, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(27, 2, '中区', 'http://www.city.yokohama.lg.jp/naka/', 'http://linkdata.org/work/rdf1s4879i', 'http://www.city.yokohama.lg.jp/kodomo/unei/nyusho-jokyo.html', NULL, 0, 35.42557850, 139.62338480, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(28, 2, '南区', 'http://www.city.yokohama.lg.jp/minami/', 'http://linkdata.org/work/rdf1s4879i', 'http://www.city.yokohama.lg.jp/kodomo/unei/nyusho-jokyo.html', NULL, 0, 35.42624150, 139.58724020, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(29, 2, '港南区', 'http://www.city.yokohama.lg.jp/konan/', 'http://linkdata.org/work/rdf1s4879i', 'http://www.city.yokohama.lg.jp/kodomo/unei/nyusho-jokyo.html', NULL, 0, 35.39275790, 139.54619780, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(30, 2, '保土ケ谷区', 'http://www.city.yokohama.lg.jp/hodogaya/', 'http://linkdata.org/work/rdf1s4879i', 'http://www.city.yokohama.lg.jp/kodomo/unei/nyusho-jokyo.html', NULL, 0, 35.46475370, 139.54169980, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(31, 2, '旭区', 'http://www.city.yokohama.lg.jp/asahi/', 'http://linkdata.org/work/rdf1s4879i', 'http://www.city.yokohama.lg.jp/kodomo/unei/nyusho-jokyo.html', NULL, 0, 35.47614910, 139.49325310, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(32, 2, '磯子区', 'http://www.city.yokohama.lg.jp/isogo/', 'http://linkdata.org/work/rdf1s4879i', 'http://www.city.yokohama.lg.jp/kodomo/unei/nyusho-jokyo.html', NULL, 0, 35.39140670, 139.58236000, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(33, 2, '金沢区', 'http://www.city.yokohama.lg.jp/kanazawa/', 'http://linkdata.org/work/rdf1s4879i', 'http://www.city.yokohama.lg.jp/kodomo/unei/nyusho-jokyo.html', NULL, 0, 35.35164030, 139.58797870, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(34, 2, '港北区', 'http://www.city.yokohama.lg.jp/kohoku/', 'http://linkdata.org/work/rdf1s4879i', 'http://www.city.yokohama.lg.jp/kodomo/unei/nyusho-jokyo.html', NULL, 0, 35.52618730, 139.58534050, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(35, 2, '緑区', 'http://www.city.yokohama.lg.jp/midori/', 'http://linkdata.org/work/rdf1s4879i', 'http://www.city.yokohama.lg.jp/kodomo/unei/nyusho-jokyo.html', NULL, 0, 35.51547310, 139.49696940, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(36, 2, '青葉区', 'http://www.city.yokohama.lg.jp/aoba/', 'http://linkdata.org/work/rdf1s4879i', 'http://www.city.yokohama.lg.jp/kodomo/unei/nyusho-jokyo.html', NULL, 0, 35.56029800, 139.48294380, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(37, 2, '都筑区', 'http://www.city.yokohama.lg.jp/tsuzuki/', 'http://linkdata.org/work/rdf1s4879i', 'http://www.city.yokohama.lg.jp/kodomo/unei/nyusho-jokyo.html', NULL, 0, 35.54134180, 139.54243440, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(38, 2, '戸塚区', 'http://www.city.yokohama.lg.jp/totsuka/', 'http://linkdata.org/work/rdf1s4879i', 'http://www.city.yokohama.lg.jp/kodomo/unei/nyusho-jokyo.html', NULL, 0, 35.40244690, 139.49514620, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(39, 2, '栄区', 'http://www.city.yokohama.lg.jp/sakae/', 'http://linkdata.org/work/rdf1s4879i', 'http://www.city.yokohama.lg.jp/kodomo/unei/nyusho-jokyo.html', NULL, 0, 35.35987470, 139.53697260, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(40, 2, '泉区', 'http://www.city.yokohama.lg.jp/izumi/', 'http://linkdata.org/work/rdf1s4879i', 'http://www.city.yokohama.lg.jp/kodomo/unei/nyusho-jokyo.html', NULL, 0, 35.41874120, 139.46697280, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000'),
	(41, 2, '瀬谷区', 'http://www.city.yokohama.lg.jp/seya/', 'http://linkdata.org/work/rdf1s4879i', 'http://www.city.yokohama.lg.jp/kodomo/unei/nyusho-jokyo.html', NULL, 0, 35.46946460, 139.45306240, '2017-11-19 11:03:22.890000', '2018-10-28 04:48:42.000000');
