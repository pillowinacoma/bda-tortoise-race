package fr.univlyon1.bda;


import fr.univlyon1.bda.extern.RaceServiceREST;
import fr.univlyon1.bda.modele.RaceMoment;

public class App {

    public static void main(String[] args) {
        System.out.println("START APPLICATION...");

        RaceServiceREST raceServiceREST = new RaceServiceREST();

        try {
            RaceMoment raceMoment = raceServiceREST.getRaceMoment();
            raceMoment.print();
        } catch (Exception e) {
            e.printStackTrace();
        }

    }
}
