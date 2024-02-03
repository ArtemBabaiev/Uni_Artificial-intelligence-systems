package edu.ais.lab6;

import java.util.Collections;
import java.util.List;

import org.javatuples.Triplet;

public class Lab6Main {

	static Triplet<Double, Double, Double> deadHotKs = Triplet.with(50.0, 9.0, 10.0);
	static Triplet<Double, Double, Double> hotKs = Triplet.with(32.0, 8.0, 10.0);
	static Triplet<Double, Double, Double> okKs = Triplet.with(20.0, 3.0, 6.0);
	static Triplet<Double, Double, Double> coldKs = Triplet.with(-9.0, 25.0, 12.0);
	static Triplet<Double, Double, Double> deadColdKs = Triplet.with(-140.0, 105.0, 400.0);

	public static void main(String[] args) {
		double temp = 18;
		List<Double> mus = List.of(
				calcMu(temp, deadHotKs),
				calcMu(temp, hotKs),
				calcMu(temp, okKs),
				calcMu(temp, coldKs),
				calcMu(temp, deadColdKs)
				);
		System.out.println(mus);
		var max = Collections.max(mus);
		System.out.println(How.getHow(max) + " " + What.getWhat(mus));
	}

	private static double calcMu(double value, Triplet<Double, Double, Double> ks) {
		double k1 = ks.getValue0();
		double k2 = ks.getValue1();
		double k3 = ks.getValue2();
		return 1 / (1 + Math.pow((value - k1) / k2, k3));
	}

	enum What {
		DEAD, COLD, OK, HOT;

		public static What getWhat(List<Double> values) {
			var index = values.indexOf(Collections.max(values));
			switch (index) {
			case 1 -> {
				return HOT;
			}
			case 2 -> {
				return OK;
			}
			case 3 -> {
				return COLD;
			}
			default -> {
				return DEAD;
			}
			}
		}
	}

	enum How {
		NOT, VERY, MORE_OR_LESS;

		public static How getHow(double value) {
			var values = List.of(1 - value, Math.pow(value, 2), Math.sqrt(value));
			var index = values.indexOf(Collections.max(values));
			switch (index) {
			case 0 -> {
				return NOT;
			}
			case 1 -> {
				return VERY;
			}
			default -> {
				return MORE_OR_LESS;
			}
			}
		}
	}
}
