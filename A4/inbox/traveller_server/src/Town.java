package src;
/**
 * Representation for a Town
 */
public class Town {
    private String name;
    private String character;

    public Town(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public String getCharacter() {
        return character;
    }

    public void setCharacter(String character) {
        this.character = character;
    }

    @Override
    public boolean equals(Object o) {
        if (o == this) {
            return true;
        }

        if (!(o instanceof Town)) {
            return false;
        }

        Town t = (Town) o;

        return t.name.equals(this.name);
    }

    @Override
    public int hashCode() {
        return name.hashCode();
    }
}
