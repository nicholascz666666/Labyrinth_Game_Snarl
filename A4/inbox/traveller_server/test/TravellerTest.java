package test;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertThrows;
import static org.junit.Assert.assertTrue;

import java.util.Arrays;
import java.util.Dictionary;
import java.util.Hashtable;
import java.util.List;

import org.junit.Test;

import src.Town;
import src.Traveller;

public class TravellerTest {

    Traveller empty;
    Traveller trav;

    Town town1;
    Town town2;
    Town town3;
    Town town4;

    Dictionary<Town, List<String>> network1;
    Dictionary<Town, List<String>> badNetwork;

    public void setUp() {
        empty = new Traveller();
        trav = new Traveller();

        town1 = new Town("town1");
        town2= new Town("town2");
        town3 = new Town("town3");
        town4 = new Town("town4");

        town1.setCharacter("Bob");
        town4.setCharacter("Joan");

        network1 = new Hashtable<Town, List<String>>();
        network1.put(town1, Arrays.asList("town2", "town4"));
        network1.put(town2, Arrays.asList("town1"));
        network1.put(town3, Arrays.asList("town4"));
        network1.put(town4, Arrays.asList("town3"));

        badNetwork = new Hashtable<Town, List<String>>();
        badNetwork.put(town1, Arrays.asList("town2, garbage"));
    }

    @Test
    public void cannotAddBadNetwork() {
        setUp();
        assertThrows(IllegalArgumentException.class, (() -> empty.createNewNetwork(badNetwork)));
    }

    @Test
    public void cannotUseUninitializedNetwork() {
        setUp();
        assertThrows(IllegalArgumentException.class, (() -> empty.setCharacter("blah", "blah")));
        assertThrows(IllegalArgumentException.class, (() -> empty.arrive("blah", "blah")));
        assertThrows(IllegalArgumentException.class, (() -> empty.modifyNetwork(network1)));
    }

    @Test
    public void canCreateNetwork() {
        setUp();
        trav.createNewNetwork(network1);

        assertTrue(trav.arrive("town2", "Bob"));
        assertFalse(trav.arrive("town3", "Bob"));
        assertFalse(trav.arrive("town2", "Joan"));
        assertFalse(trav.arrive("town2", "blah"));
    }

    @Test
    public void canSetCharacter() {
        setUp();
        trav.createNewNetwork(network1);
        assertTrue(trav.arrive("town2", "Bob"));
        trav.setCharacter("Greg", "town2");
        assertFalse(trav.arrive("town2", "Bob"));
    }


}