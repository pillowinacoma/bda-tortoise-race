package fr.univlyon1.bda.modele;

public class Tortoise {

    private int id;
    private int top;
    private int position;

    public Tortoise(int id, int top, int position) {
        this.id = id;
        this.top = top;
        this.position = position;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getTop() {
        return top;
    }

    public void setTop(int top) {
        this.top = top;
    }

    public int getPosition() {
        return position;
    }

    public void setPosition(int position) {
        this.position = position;
    }
}
