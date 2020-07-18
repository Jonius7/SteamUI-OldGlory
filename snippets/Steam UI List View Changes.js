 List View Only 
.cssgrid_CSSGrid_3vHkm.libraryhomeshowcases_ShowcaseGrid_3DJLG, .appgrid_YourCollection_11p6F {
    grid-template-columns: repeat(auto-fill, 1000px) !important;
	grid-auto-rows: 46.5px !important;
}

.appportrait_LibraryItemBox_WYgDg {
    width: 10%;
}

.appportrait_LibraryItemBoxSubscript_1LJqx {

    margin-left: 115px;
}



=====
JS

                    switch (i) {	
						case 4: case 5: case 9: case 6:
                            if (0 == t.minutes_playtime_forever) {a = ''; return null;}
                            a = zp(t.minutes_playtime_forever);
							if (!t.GetLastTimePlayed()) {b = ''; return null;}
                            b = Object(Lt.m)(t.GetLastTimePlayed());					
							var s = t.metacritic_score;
                            if (void 0 === s) {c = 0}
							c = s;
							if (null == t.size_on_disk) {d = 0}
                            d = Object(Dd.a)(parseFloat(t.size_on_disk), 2), null != t.library_id && (d = t.library_id + " " + d);
                            break;
						
                        /*case 4:
                            if (0 == t.minutes_playtime_forever) return null;
                            a = zp(t.minutes_playtime_forever);
							var s = t.metacritic_score;
                            if (void 0 === s) return null; 
							b = s;
                            break;*/
                        /*case 5:
                            if (!t.GetLastTimePlayed()) return null;
                            a = Object(Lt.m)(t.GetLastTimePlayed());
                            break;*/
                        /*case 9:
                            var s = t.metacritic_score;
                            if (void 0 === s) return null;
                            o = GM.a.MCGreen, s < 70 && 49 < s ? o = GM.a.MCOrange : s < 50 && (o = GM.a.MCRed), a = s;
                            break;*/
                        case 6:
                            if (0 == t.GetCanonicalReleaseDate()) return null;
                            a = Object(Lt.l)(t.GetCanonicalReleaseDate());
                            break;
                        case 8:
                            if (null == t.size_on_disk) return null;
                            a = Object(Dd.a)(parseFloat(t.size_on_disk), 2), null != t.library_id && (a = t.library_id + " " + a);
                            break;
                        case 2:
                            a = jM.BGameHasAchievements(t.appid) ? (r = jM.GetAchievementProgress(t.appid), Object(Lt.d)("#Library_SortByPctAchievementsComplete_Tag", Math.floor(r))) : Object(Lt.d)("#Library_SortByPctAchievementsNoAchievements_Tag");
                            break;
                        case 11:
                            var l = t.review_score,
                                c = t.review_percentage;
                            if (!l) return null;
                            a = j.createElement("span", null, Object(Lt.d)("#SteamReviewScore_" + l), " - ", c, "%"), o = 5 < l ? GM.a.SteamReviewPositive : l < 5 ? GM.a.SteamReviewNegative : GM.a.SteamReviewMixed, o = Object(oa.a)(GM.a.SteamReview, o);
                            break;
                        case 10:
							
                        default:
                            return null
                    }
                    return j.createElement("div", {
                        className: Object(oa.a)(GM.a.LibraryItemBoxSubscript, o)
                    }, "Hours Played: ".concat(a," | Last Played: ", b, " | Metacritic: ", c, " | Size on Disk: ", d))
                }),