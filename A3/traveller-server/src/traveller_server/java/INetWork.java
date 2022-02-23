package traveller_server.java;

import java.util.List;

// The interface network of node which is town.
public interface INetWork {
    /**
     * add a new town to a network.
     * @param townName the name of town will be added to the network.
     */
    void addTown(String townName);

    /**
     * place a character in a town.
     * If the town doesn't exist, throw an exception.
     * If the character already exists in the Network
     * it should be placed at the new location and removed from it's previous location.
     * @param townName the name of the town to place a character.
     * @param characterName the name of the character will be placed.
     */
    void placeCharacter(String townName, String characterName);

    /**
     * get the names of characters that are currently in a town.
     * If no characters are in the town, return an empty list.
     * If the town doesn't exist, throw an exception.
     * @param townName the name of the town.
     * @return the names of characters that are currently in the town with given name.
     */
    List<String> getCharactersInTown(String townName);

    /**
     * query whether a path exists between the character's current town and the given town that contains only nodes with no characters. If a path does exist it returns true. If not, it returns false. If the town or character doesn't exist, throw an exception.
     * @param destinationTown
     * @param characterName
     * @return whether a path exists between the character's current town
     * and the given town that contains only nodes with no characters.
     */
    boolean characterlessPathExists(String destinationTown, String characterName);


    /**
     * add the path from a town to a town.
     * @param from the from town.
     * @param to the destination town.
     */
    public void addPath(String from, List<String> to);
}
