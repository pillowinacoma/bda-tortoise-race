package fr.univlyon1.bda.modele;


import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.OneToMany;
import java.util.Collection;

@Entity
public class RaceMoment {

    @Id
    private int top;

    private float quality;
    private float temperature;

    @OneToMany
    private Collection<Tortoise> tortoises;


    public RaceMoment() {
    }

    public RaceMoment(float quality, float temperature, Collection<Tortoise> tortoises) {
        this.quality = quality;
        this.temperature = temperature;
        this.tortoises = tortoises;
    }

    public void print() {
        int i = 0;
        String str = "";
        while (i < tortoises.size() || i < 10) {
            // str += "        { \"id\": " + tortoises.(i).getId() + ", \"top\": " + tortoises[i].getTop() + ", \"position\": " + tortoises[i].getPosition() + " },\n";
            i++;
        }
        System.out.println("\n" +
                "{\n" +
                "    tortoises : [\n" +
                str +
                "    ]," +
                "    qualite : " + quality + "\n" +
                "    temperature : " + temperature + "\n" +
                "}");
    }

    public float getQuality() {
        return quality;
    }

    public void setQuality(float quality) {
        this.quality = quality;
    }

    public float getTemperature() {
        return temperature;
    }

    public void setTemperature(float temperature) {
        this.temperature = temperature;
    }

    public Collection<Tortoise> getTortoises() {
        return tortoises;
    }

    public void setTortoises(Collection<Tortoise> tortoises) {
        this.tortoises = tortoises;
    }
}
