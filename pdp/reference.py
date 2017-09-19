
class ArtifactReference:
    references = {}

    def get_artifact_reference_path(self, key):
        if key not in self.references:
            raise ValueError('artifact references does not have key:' + key)
        return ArtifactReference.references[key]
