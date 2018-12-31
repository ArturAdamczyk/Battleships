from battleships.models.submarine import Submarine
from battleships.models.carrier import Carrier
from battleships.models.destroyer import Destroyer
from battleships.models.frigate import Frigate
from battleships.models.coordinate import Coordinate


class TestDataSet:

    @staticmethod
    def __ship_set_1():
        carrier = Carrier(name="1")
        carrier.save()
        Coordinate(x=1, y=4, carrier=carrier).save()
        Coordinate(x=2, y=4, carrier=carrier).save()
        Coordinate(x=3, y=4, carrier=carrier).save()
        Coordinate(x=4, y=4, carrier=carrier).save()
        destroyer = Destroyer(name="2")
        destroyer.save()
        Coordinate(x=2, y=7, destroyer=destroyer).save()
        Coordinate(x=3, y=7, destroyer=destroyer).save()
        Coordinate(x=4, y=7, destroyer=destroyer).save()
        frigate = Frigate(name="3")
        frigate.save()
        Coordinate(x=3, y=3, frigate=frigate).save()
        Coordinate(x=4, y=3, frigate=frigate).save()
        submarine = Submarine(name="4")
        submarine.save()
        Coordinate(x=5, y=5, submarine=submarine).save()
        return [carrier, destroyer, frigate, submarine]

    @staticmethod
    def __ship_set_2():
        carrier = Carrier(name="5")
        carrier.save()
        Coordinate(x=18, y=2, carrier=carrier).save()
        Coordinate(x=17, y=2, carrier=carrier).save()
        Coordinate(x=16, y=2, carrier=carrier).save()
        Coordinate(x=15, y=2, carrier=carrier).save()
        destroyer = Destroyer(name="6")
        destroyer.save()
        Coordinate(x=12, y=5, destroyer=destroyer).save()
        Coordinate(x=13, y=5, destroyer=destroyer).save()
        Coordinate(x=14, y=5, destroyer=destroyer).save()
        frigate = Frigate(name="7")
        frigate.save()
        Coordinate(x=15, y=10, frigate=frigate).save()
        Coordinate(x=16, y=10, frigate=frigate).save()
        submarine = Submarine(name="8")
        submarine.save()
        Coordinate(x=10, y=8, submarine=submarine).save()
        return [carrier, destroyer, frigate, submarine]

    @staticmethod
    def __ship_set_3():
        carrier = Carrier(name="9")
        carrier.save()
        Coordinate(x=1, y=20, carrier=carrier).save()
        Coordinate(x=2, y=20, carrier=carrier).save()
        Coordinate(x=3, y=20, carrier=carrier).save()
        Coordinate(x=4, y=20, carrier=carrier).save()
        destroyer = Destroyer(name="10")
        destroyer.save()
        Coordinate(x=3, y=19, destroyer=destroyer).save()
        Coordinate(x=4, y=19, destroyer=destroyer).save()
        Coordinate(x=5, y=19, destroyer=destroyer).save()
        frigate = Frigate(name="11")
        frigate.save()
        Coordinate(x=2, y=17, frigate=frigate).save()
        Coordinate(x=3, y=17, frigate=frigate).save()
        submarine = Submarine(name="12")
        submarine.save()
        Coordinate(x=10, y=12, submarine=submarine).save()
        return [carrier, destroyer, frigate, submarine]

    @staticmethod
    def __ship_set_4():
        carrier = Carrier(name="13")
        carrier.save()
        Coordinate(x=15, y=18, carrier=carrier).save()
        Coordinate(x=14, y=18, carrier=carrier).save()
        Coordinate(x=13, y=18, carrier=carrier).save()
        Coordinate(x=12, y=18, carrier=carrier).save()
        destroyer = Destroyer(name="14")
        destroyer.save()
        Coordinate(x=20, y=17, destroyer=destroyer).save()
        Coordinate(x=19, y=17, destroyer=destroyer).save()
        Coordinate(x=18, y=17, destroyer=destroyer).save()
        frigate = Frigate(name="15")
        frigate.save()
        Coordinate(x=15, y=15, frigate=frigate).save()
        Coordinate(x=16, y=15, frigate=frigate).save()
        submarine = Submarine(name="16")
        submarine.save()
        Coordinate(x=12, y=19, submarine=submarine).save()
        return [carrier, destroyer, frigate, submarine]

    @staticmethod
    def get_ships_set(choice):
        if choice == 1:
            return TestDataSet.__ship_set_1()
        elif choice == 2:
            return TestDataSet.__ship_set_2()
        elif choice == 3:
            return TestDataSet.__ship_set_3()
        else:
            return TestDataSet.__ship_set_4()