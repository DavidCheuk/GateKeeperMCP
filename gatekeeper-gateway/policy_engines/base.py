
class PolicyEnginePlugin:
    def evaluate(self, context: dict, action: str, resource: str, **kwargs) -> dict:
        """
        Evaluate the policy for the given context, action, and resource.
        Return: {'allow': bool, 'reason': str}
        """
        raise NotImplementedError("Must implement evaluate in subclass.")
