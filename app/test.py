import matplotlib.pyplot as plt
from models import Card
def graphs_of_list(list_id):
    cards = Card.query.filter_by(list_id=list_id).all()
    x = []
    y = []
    for card in cards:
        if card.Completed:
            x.append(card.complete_time)
            i = Card.query.filter_by(complete_time=card.complete_time).all()
            y.append(len(i))
    plt.plot(x,y)
    plt.show()