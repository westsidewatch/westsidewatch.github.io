import unittest

from dore_core.bible.query_planner import plan_bible_query


class BibleQueryPlannerTests(unittest.TestCase):
    def test_reference_first_without_model(self):
        plan = plan_bible_query("馬太福音 6:33 先求他的國和義")
        self.assertEqual(plan.intent, "reference")
        self.assertEqual(plan.lanes[:2], ("reference", "biblical_world"))
        self.assertFalse(plan.semantic_allowed)
        self.assertFalse(plan.large_model_required)
        self.assertFalse(plan.model_invoked)
        self.assertEqual(plan.execution_level, "L1-retrieval")

    def test_geography_uses_world_before_documents(self):
        plan = plan_bible_query("基列的雅比城在哪裡？")
        self.assertEqual(plan.intent, "geography")
        self.assertEqual(plan.lanes[:2], ("geography", "biblical_world"))
        self.assertLess(plan.lanes.index("biblical_world"), plan.lanes.index("document"))

    def test_entity_count_uses_entity_reflex(self):
        plan = plan_bible_query("聖經中一共有幾位馬利亞？")
        self.assertEqual(plan.intent, "entity")
        self.assertEqual(plan.lanes[0], "entity")
        self.assertFalse(plan.model_invoked)

    def test_interpretive_query_marks_reasoning_without_invoking_model(self):
        plan = plan_bible_query("為什麼馬太把這段放在這裡？")
        self.assertTrue(plan.reasoning_allowed)
        self.assertEqual(plan.execution_level, "L3-reasoning")
        self.assertFalse(plan.model_invoked)

    def test_deep_escalation_is_explicit_and_observable(self):
        plan = plan_bible_query("嗎哪和約翰福音六章有什麼關係？", deep=True)
        self.assertTrue(plan.semantic_allowed)
        self.assertTrue(plan.reasoning_allowed)
        self.assertEqual(plan.lanes[-2:], ("semantic", "reasoning"))
        self.assertEqual(plan.escalation_policy, "lowest-sufficient-capability")


if __name__ == "__main__":
    unittest.main()
