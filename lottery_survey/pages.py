from otree.api import Page
from .models import Constants, Player, Subsession
import random
from iomotions.otree.pages import ScenePage


class Roulette_1(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        # Initialize selected_round and p if not set
        if self.player.field_maybe_none('selected_round') is None:
            self.player.selected_round = random.randint(1, Constants.num_rounds)

        if self.player.field_maybe_none('p') is None:
            self.player.p = random.uniform(0, 100)

        selected_round = self.player.selected_round
        p = round(self.player.p, 2)
        one_minus_p = round(100 - p, 2)

        player_in_selected_round = self.player.in_round(selected_round)

        # Determine scenario and round index
        scenario_index = (selected_round - 1) // 9
        round_in_scenario = (selected_round - 1) % 9
        scenario = Constants.scenarios[scenario_index]

        # Get alpha value safely
        alpha = player_in_selected_round.field_maybe_none('alpha')
        if alpha is None:
            alpha = 1  # Default value if missing
        alpha = round(alpha, 2)
        one_minus_alpha = round(1 - alpha, 2)

        # Get scenario-specific values
        x1_l = round(scenario['x1_l_values'][round_in_scenario], 1)
        x1_h = round(scenario['x1_h_values'][round_in_scenario], 1)
        x2_l = round(scenario['x2_l_values'][round_in_scenario], 1)
        x2_h = round(scenario['x2_h_values'][round_in_scenario], 1)

        return {
            'selected_round': selected_round,
            'p': p,
            'one_minus_p': one_minus_p,
            'alpha': alpha,
            'one_minus_alpha': one_minus_alpha,
            'x1_l': x1_l,
            'x1_h': x1_h,
            'x2_l': x2_l,
            'x2_h': x2_h,
            'Constants': Constants,
        }

class ConsentForm(Page):
    form_model = 'player'
    form_fields = ['consent_age', 'consent_read', 'consent_participate']
    def is_displayed(self):
        return self.round_number == 1


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1


class PracticeRound(Page):
    # class PracticeRound(ScenePage):
    form_model = 'player'
    form_fields = ['alpha']

    def is_displayed(self):
        return self.round_number == 1  # Only show on the first round

    def vars_for_template(self):
        scenario = Constants.practice_scenarios[0]

        # Store the practice round number and scenario
        self.player.original_round_number = self.round_number
        self.player.original_scenario_number = 1

        # Use the first set of values
        p = round(scenario['p_values'][0], 2)
        one_minus_p = round(scenario['one_minus_p_values'][0], 2)

        # Get rounded values
        x1_l = round(scenario['x1_l_values'][0], 2)
        x1_h = round(scenario['x1_h_values'][0], 2)
        x2_l = round(scenario['x2_l_values'][0], 2)
        x2_h = round(scenario['x2_h_values'][0], 2)

        # Format currency values for display
        x1_l_formatted = f"-${abs(x1_l)}" if x1_l < 0 else f"${x1_l}"
        x1_h_formatted = f"-${abs(x1_h)}" if x1_h < 0 else f"${x1_h}"
        x2_l_formatted = f"-${abs(x2_l)}" if x2_l < 0 else f"${x2_l}"
        x2_h_formatted = f"-${abs(x2_h)}" if x2_h < 0 else f"${x2_h}"

        vars_dict = {
            'round_number': self.round_number,
            'num_rounds': 1,  # Ensure it's just one round
            'scenario_number': 1,
            'round_in_scenario': 1,
            'p': p,
            'one_minus_p': one_minus_p,
            'x1_l': x1_l,
            'x1_h': x1_h,
            'x2_l': x2_l,
            'x2_h': x2_h,
            'x1_l_formatted': x1_l_formatted,
            'x1_h_formatted': x1_h_formatted,
            'x2_l_formatted': x2_l_formatted,
            'x2_h_formatted': x2_h_formatted,
        }

        # Store values in player model for later access
        self.player.p = p
        self.player.one_minus_p = one_minus_p
        self.player.x1_l = x1_l
        self.player.x1_h = x1_h
        self.player.x2_l = x2_l
        self.player.x2_h = x2_h

        return vars_dict




class LotterySurvey(ScenePage):
#class LotterySurvey(Page):

    form_model = 'player'
    form_fields = ['alpha']

    def vars_for_template(self):
        # Ensure shuffled_rounds exists
        if 'shuffled_rounds' not in self.session.vars:
            self.session.vars['shuffled_rounds'] = Subsession.generate_shuffled_rounds()

        shuffled_round = self.session.vars['shuffled_rounds'][self.round_number - 1]

        # Store the original round number and scenario in player's model
        self.player.original_round_number = shuffled_round

        scenario_index = (shuffled_round - 1) // 9
        round_in_scenario = (shuffled_round - 1) % 9
        scenario = Constants.scenarios[scenario_index]

        # Save original scenario number
        self.player.original_scenario_number = scenario_index + 1

        # Calculate p and one_minus_p with rounding to avoid floating-point precision issues
        p = round(scenario['p_values'][round_in_scenario], 2)
        one_minus_p = round(100 - p, 2)

        # Store values in player model
        self.player.p = p
        self.player.one_minus_p = one_minus_p
        self.player.x1_l = round(scenario['x1_l_values'][round_in_scenario], 2)
        self.player.x1_h = round(scenario['x1_h_values'][round_in_scenario], 2)
        self.player.x2_l = round(scenario['x2_l_values'][round_in_scenario], 2)
        self.player.x2_h = round(scenario['x2_h_values'][round_in_scenario], 2)

        # Format currency values for display
        x1_l = self.player.x1_l
        x1_h = self.player.x1_h
        x2_l = self.player.x2_l
        x2_h = self.player.x2_h

        x1_l_formatted = f"-${abs(x1_l)}" if x1_l < 0 else f"${x1_l}"
        x1_h_formatted = f"-${abs(x1_h)}" if x1_h < 0 else f"${x1_h}"
        x2_l_formatted = f"-${abs(x2_l)}" if x2_l < 0 else f"${x2_l}"
        x2_h_formatted = f"-${abs(x2_h)}" if x2_h < 0 else f"${x2_h}"

        # Safely retrieve alpha using field_maybe_none
        alpha = self.player.field_maybe_none('alpha')

        # Create and return the dictionary with all variables needed for the template
        vars_dict = {
            'round_number': self.round_number,
            'original_round_number': shuffled_round,
            'num_rounds': 45,
            'scenario_number': scenario_index + 1,
            'round_in_scenario': round_in_scenario + 1,
            'p': p,
            'one_minus_p': one_minus_p,
            'x1_l': x1_l,
            'x1_h': x1_h,
            'x2_l': x2_l,
            'x2_h': x2_h,
            'x1_l_formatted': x1_l_formatted,
            'x1_h_formatted': x1_h_formatted,
            'x2_l_formatted': x2_l_formatted,
            'x2_h_formatted': x2_h_formatted,
        }

        # Add values that depend on alpha only if it exists
        if alpha is not None:
            investment_2_amount = round(1 - alpha, 2)
            player_alpha_formatted = f"-${abs(alpha)}" if alpha < 0 else f"${alpha}"
            investment_2_amount_formatted = (
                f"-${abs(investment_2_amount)}" if investment_2_amount < 0 else f"${investment_2_amount}"
            )

            vars_dict.update({
                'player_alpha_formatted': player_alpha_formatted,
                'investment_2_amount': investment_2_amount,
                'investment_2_amount_formatted': investment_2_amount_formatted
            })

        return vars_dict


class CognitiveUncertainty(Page):
    form_model = 'player'
    form_fields = ['certainty']

    def vars_for_template(self):
        # Format the currency values directly in the context
        x1_l = self.player.x1_l
        x1_h = self.player.x1_h
        x2_l = self.player.x2_l
        x2_h = self.player.x2_h

        # Handle the case where alpha might be None
        player_alpha = self.player.alpha if self.player.alpha is not None else 0
        investment_2_amount = round(1 - player_alpha, 2) if player_alpha is not None else 0

        # Format currency values for display
        x1_l_formatted = f"-${abs(x1_l)}" if x1_l < 0 else f"${x1_l}"
        x1_h_formatted = f"-${abs(x1_h)}" if x1_h < 0 else f"${x1_h}"
        x2_l_formatted = f"-${abs(x2_l)}" if x2_l < 0 else f"${x2_l}"
        x2_h_formatted = f"-${abs(x2_h)}" if x2_h < 0 else f"${x2_h}"
        player_alpha_formatted = f"-${abs(player_alpha)}" if player_alpha < 0 else f"${player_alpha}"
        investment_2_amount_formatted = f"-${abs(investment_2_amount)}" if investment_2_amount < 0 else f"${investment_2_amount}"

        return {
            'p': int(self.player.p),
            'one_minus_p': int(self.player.one_minus_p),
            'x1_l_formatted': x1_l_formatted,
            'x1_h_formatted': x1_h_formatted,
            'x2_l_formatted': x2_l_formatted,
            'x2_h_formatted': x2_h_formatted,
            'player_alpha_formatted': player_alpha_formatted,
            'investment_2_amount_formatted': investment_2_amount_formatted,
            'round_number': self.round_number,
            'num_rounds': 45,
            'investment_2_amount': investment_2_amount,
            'x1_l': x1_l,
            'x1_h': x1_h,
            'x2_l': x2_l,
            'x2_h': x2_h,
            'player': self.player
        }



class ConsentForm(Page):
    form_model = 'player'
    form_fields = ['consent_age', 'consent_read', 'consent_participate']

    def is_displayed(self):
        return self.round_number == 1
    def error_message(self, values):
        if not (values['consent_age'] and values['consent_read'] and values['consent_participate']):
            return 'Debe aceptar todos los elementos de consentimiento para continuar.'

class example_combined(Page):
    def is_displayed(self):
        return self.round_number == 1

class example(Page):
    def is_displayed(self):
        return self.round_number == 1

class example2(Page):
    def is_displayed(self):
        return self.round_number == 1

class example22(Page):
    def is_displayed(self):
        return self.round_number == 1


class example222(Page):
    def is_displayed(self):
        return self.round_number == 1


class example3(Page):
    def is_displayed(self):
        return self.round_number == 1

class earning(Page):
    def is_displayed(self):
        return self.round_number == 1

class example4(Page):
    def is_displayed(self):
        return self.round_number == 1

class welcome(Page):
    def is_displayed(self):
        return self.round_number == 1

class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

class Introduction2(Page):
    def is_displayed(self):
        return self.round_number == 1


class SurveyIntroduc(Page):
    template_name = 'lottery_survey/SurveyIntroduc.html'

    def is_displayed(self):
        return self.round_number == Constants.individual_rounds + 4


class Demographics(Page):
    form_model = 'player'
    form_fields = ['age_check', 'gender', 'career', 'native_language', 'university_year', 'gpa', 'smoker', 'alcohol', 'drugs', 'weekly_spending']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

class CognitiveReflectionTest(Page):
    form_model = 'player'
    form_fields = ['crt_linda', 'crt_bat', 'crt_widget', 'crt_lake', 'crt_double']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

class FinancialLiteracy(Page):
    form_model = 'player'
    form_fields = ['q_interest_rates', 'q_inflation', 'q_risk_diversification', 'q_probability']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class RiskAttitudes(Page):
    form_model = 'player'
    form_fields = ['risk_general', 'risk_driving', 'risk_career', 'risk_health']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

class DecisionMakingScenarios(Page):
    form_model = 'player'
    form_fields = ['scenario_jar', 'monty_hall']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class MatrixReasoning(Page):
    form_model = 'player'
    form_fields = ['Matrix_B09', 'Matrix_B11', 'Matrix_C02', 'Matrix_C05',
                   'Matrix_C12', 'Matrix_D05', 'Matrix_D07', 'Matrix_E07']
    def is_displayed(self):
        return self.round_number == Constants.num_rounds






class EndPage(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def before_next_page(self):
        self.player.exit_survey_completed = True
    pass


class ComprehensionCheck(Page):
    form_model = 'player'
    form_fields = ['question_1', 'question_2', 'question_3']

    def is_displayed(self):
        return self.round_number == 1

    def error_message(self, values):
        errors = {}
        if values['question_1'] != '$0.20':
            errors['question_1'] = 'This answer is incorrect'
            if values['question_2'] != "One always gains when the other loses":
                errors['question_2'] = 'This answer is incorrect'

        if values['question_3'] != "The chances of each possibility can change from round to round.":
            errors['question_3'] = 'This answer is incorrect'
        if errors:
            return errors
        else:
            # If no errors, set passed_comprehension to True
            self.player.passed_comprehension = True
            return None

    def vars_for_template(self):
        return {
            'show_success': self.player.passed_comprehension if hasattr(self.player, 'passed_comprehension') else False
        }




class EarningsExplanation(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == 1  # Only show on the first round


# Add these updates to your pages.py file:



# Define the initial sequence
initial_sequence = [
    welcome,
    Introduction2,
    Introduction,
    example,
    example2,
    example22,
    example222,
    example3,
]

practice_rounds = [PracticeRound]

# Define the main experiment sequence
main_sequence = [
   ComprehensionCheck,
    EarningsExplanation,
    LotterySurvey,
    CognitiveUncertainty,
    SurveyIntroduc,
    Demographics,
    CognitiveReflectionTest,
    MatrixReasoning,
    FinancialLiteracy,
    RiskAttitudes,
    DecisionMakingScenarios,
    Roulette_1
]

# Combine all sequences
page_sequence = initial_sequence + practice_rounds + main_sequence