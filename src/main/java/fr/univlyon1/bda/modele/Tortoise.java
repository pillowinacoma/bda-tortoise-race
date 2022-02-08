package fr.univlyon1.bda.modele;

import javax.persistence.*;

@Entity
@Table(name = "tortoises")
public class Tortoise {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private int id;

    @Column(name = "top")
    private int top;
    @Column(name = "position")
    private int position;

    public Tortoise() {}
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
