package traveller_server.java;

/**
 * The class to represent a Character.
 */
public class Character {
    // the name of character.
    private String name;

    // the address of character.
    private String address;

    /**
     * Get the name of the character.
     * @return the name of the character.
     */
    public String getName() {
        return name;
    }

    /**
     * Set the name of the character.
     * @param name the name of the character.
     */
    public void setName(String name) {
        this.name = name;
    }

    /**
     * Get the address of the character.
     * @return the address of the character.
     */
    public String getAddress() {
        return address;
    }

    /**
     * Set the address of the character.
     * @param address the address of the character.
     */
    public void setAddress(String address) {
        this.address = address;
    }

    @Override
    public boolean equals(Object obj) {
        if (obj instanceof Character) {
            return ((Character)obj).getName().equals(this.name);
        }
        return false;
    }
}
