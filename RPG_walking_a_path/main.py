from myclasses import DebugDriver, Game

def main():
    zone_name = "env01"
    mydriver = Game(zone_name)
    mydriver.read_data()
    mydriver.main(2, 5)

if __name__ == "__main__":
    main()