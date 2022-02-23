package traveller_server.java;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

/**
 * the class to implement the Interface INetWork.
 */
public class NetWork implements INetWork{
    // the hashmap represent the path between the key and value.
    private HashMap<String,List<String>> towns;

    //represent all the characters in the network.
    private List<Character> characters;

    public NetWork(){
        this.towns = new HashMap();
        this.characters = new ArrayList<>();
    }


    @Override
    public void addTown(String townName) {
        if (!towns.containsKey(townName)) {
            towns.put(townName,new ArrayList<>());
        }
    }


    public void addPath(String from, List<String> to) {
        if (towns.containsKey(from)) {
            for (String s:to) {
                towns.get(from).add(s);
            }
        } else {
            towns.put(from, to);
        }
    }

    @Override
    public void placeCharacter(String townName, String characterName) {
        if (!towns.containsKey(townName)) {
            System.out.println(townName);
            throw new IllegalArgumentException("no such town");
        }
        Character temp = new Character();
        temp.setName(characterName);
        temp.setAddress(townName);
        if (!characters.contains(temp)) {
            characters.add(temp);
        } else {
            for (Character c: this.characters) {
                if (c.getName().equals(characterName)) {
                   c.setAddress(characterName);
                }
            }
        }
    }

    @Override
    public List<String> getCharactersInTown(String townName) {
        List<String> result = new ArrayList<>();
        for (Character c:characters) {
            if (c.getAddress().equals(townName)) {
                result.add(c.getAddress());
            }
        }
        return result;
    }

    @Override
    public boolean characterlessPathExists(String destinationTown, String characterName) {
        String start = null;
        List<String> visited = new ArrayList<>();
        for (Character c:characters) {
            visited.add(c.getAddress());
            if (c.getName().equals(characterName)){
                start = c.getAddress();
            }
        }
        visited.remove(start);


        return dfs(visited,towns,destinationTown, start);
    }

    /**
     * the dfs algorithm to search for a path.
     * @param visited the towns have been visited.
     * @param towns all the towns.
     * @param destinationTown the destination town.
     * @param start  the start town.
     * @return the boolean whether there is a path from start to destination without visiting
     * the visited towns.
     */
    private boolean dfs(List<String> visited, HashMap<String,List<String>> towns,
                        String destinationTown,String start) {
        if (start.equals(null)) {
            throw  new IllegalArgumentException("need a character name to start");
        }

        if (!visited.contains(start)) {
            visited.add(start);
            if (start.equals(destinationTown)) {
                return true;
            }
            boolean result = false;
            for (String t : towns.get(start)) {
                result = result || dfs(visited,towns,destinationTown,t);
            }
            return  result;
        }
        return false;
    }
}
