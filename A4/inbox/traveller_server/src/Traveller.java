package src;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Dictionary;
import java.util.Enumeration;
import java.util.List;
import java.util.stream.*;
import java.lang.IllegalArgumentException;

/**
 * Implementation of a Traveller Server
 */


 public class Traveller {

    private Dictionary<Town, List<String>> network;

    public Traveller() {
        network = null;
    }

    /**
     * Sets network for travel to the given directory if valid
     * All Strings in the Value lists must correspond to the name of a Town Key
     * @param dictionary
     */
    public void createNewNetwork(Dictionary<Town, List<String>> dictionary) {
        validateDictionaryForCreate(dictionary);
        this.network = dictionary;
    }

    public void modifyNetwork(Dictionary<Town, List<String>> dictionary) {
        if (network == null) {
            throw new IllegalArgumentException("Network has not been created yet");
        }
        validateDictionaryForUpdate(dictionary);
        for (Town town : Collections.list(dictionary.keys())) {
            network.put(town, dictionary.get(town));
        }
    }

    public void setCharacter(String name, String town) {
        if (network == null) {
            throw new IllegalArgumentException("Network has not been created yet");
        }

        Town t = getTown(town);
        if (t == null) {
            throw new IllegalArgumentException("Town " + town + " does not exist");
        }
        t.setCharacter(name);
    }

    public boolean arrive(String town, String character) {
        if (network == null) {
            throw new IllegalArgumentException("Network has not been created yet");
        }
        Town destination = getTown(town);
        return arrive(destination, character, new ArrayList<>());
    }

    private boolean arrive(Town destination, String character, List<String> visited) {
        if (visited.contains(destination.getName())) {
            return false;
        }

        if (destination.getCharacter() != null) {
            return (destination.getCharacter().equals(character));
        }

        for (String neighbor : network.get(destination)) {
            if(arrive(getTown(neighbor), character, visited)) {
                return true;
            }
            visited.add(neighbor);
        }

        return false;
    }


    private Town getTown(String name) {
        for (Town t : Collections.list(network.keys())) {
            if(t.getName().equals(name)) {
                return t;
            }
        }
        return null;
    }

    private void validateDictionaryForCreate(Dictionary<Town, List<String>> dictionary) {
        List<String> townNames = getTownNames(dictionary.keys());
        for (List<String> neighbors : Collections.list(dictionary.elements())) {
            validateNeighborsList(neighbors, townNames);
        }

    }

    private void validateDictionaryForUpdate(Dictionary<Town, List<String>> dictionary) {
        ArrayList<String> townNames = getTownNames(dictionary.keys());
        townNames.addAll(getTownNames(network.keys()));
        for (List<String> neighbors : Collections.list(dictionary.elements())) {
            validateNeighborsList(neighbors, townNames);
        }
    }

    private void validateNeighborsList(List<String> neighbors, List<String> validTowns) {
        for (String neighbor : neighbors) {
            if (!validTowns.contains(neighbor)) {
                throw new IllegalArgumentException("Neighboring town " + neighbor + " does not exist");
            }
        }
    }

    private ArrayList<String> getTownNames(Enumeration<Town> towns) {
        return (ArrayList<String>) Collections.list(towns).stream().map(t -> t.getName()).collect(Collectors.toList());
    }
 }