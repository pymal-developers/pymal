__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"


class Recommendation(object):
    def __init__(self, div):
        from pymal import Account, Anime

        recommended, recommends_divs = div.table.tbody.tr.findAll(name="td", recursive=False)

        self.recommended_anime = Anime.Anime(int(recommended.div.a["href"].split('/')[2]))

        data = recommends_divs.findAll(name="div", recursive=False)
        if 3 == len(data):
            recommends = [data[2]]
        elif 5 == len(data):
            _, _, first_recommend, _, other_recommends = data
            recommends = [first_recommend] + other_recommends.findAll(name="div", recursive=False)
        else:
            assert False, "Unknown size of data: " + str(len(data))

        self.recommends = dict()

        for recommend in recommends:
            recommend_data, user_data = recommend.findAll(name="div", recursive=False)
            username = user_data.find(name='a', recursive=False)["href"].split('/')[2]
            self.recommends[Account.Account(username)] = recommend_data.text

    def __repr__(self):
        return "<{0:s} for {1:s} by {2:d} users>".format(
            self.__class__.__name__,
            self.recommended_anime,
            len(self.recommends)
        )