package performance

import com.intuit.karate.gatling.PreDef._
import io.gatling.core.Predef._
import scala.concurrent.duration._

class OrdersSpikeTest extends Simulation {

  val protocol = karateProtocol()

  val orders = scenario("Orders Spike Test")
    .exec(karateFeature("classpath:performance/orders.feature"))

  setUp(
    orders.inject(

      // 1) Carga normal (baseline)
      constantUsersPerSec(5) during (15 seconds),

      // 2) Spike instantáneo
      atOnceUsers(500),               // PICAZO

      // 3) Mantener carga elevada breve (opcional pero recomendado)
      constantUsersPerSec(200) during (10 seconds),

      // 4) Caída repentina (ver estabilidad)
      rampUsersPerSec(200) to 10 during (15 seconds),

      // 5) Carga estable normal luego del spike
      constantUsersPerSec(10) during (20 seconds),

      // 6) Cool down final
      nothingFor(10 seconds)
    ).protocols(protocol)
  )
}
