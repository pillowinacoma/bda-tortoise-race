package fr.univlyon1.bda.modele;


public class RaceMoment {

    private float quality;
    private float temperature;
    private Tortoise[] tortoises;


    public RaceMoment(float quality, float temperature, Tortoise[] tortoises) {
        this.quality = quality;
        this.temperature = temperature;
        this.tortoises = tortoises;
    }

    public void print() {
        int i = 0;
        String str = "";
        while(i < tortoises.length || i < 10) {
            str += "        { \"id\": "+tortoises[i].getId()+", \"top\": "+tortoises[i].getTop()+", \"position\": "+tortoises[i].getPosition()+" },\n";
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

    public Tortoise[] getTortoises() {
        return tortoises;
    }

    public void setTortoises(Tortoise[] tortoises) {
        this.tortoises = tortoises;
    }
}
