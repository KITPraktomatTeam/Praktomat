import org.junit.runners.Suite;
import org.junit.runner.RunWith;

@RunWith(Suite.class)
@Suite.SuiteClasses({ {% for testclass in testclasses  %} {{testclass}}.class, {% endfor %} })
public class AllJUnitTests {
}
