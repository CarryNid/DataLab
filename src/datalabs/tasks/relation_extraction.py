# coding=utf-8
# Copyright 2022 The DataLab Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dataclasses import dataclass
from typing import ClassVar, Dict, Optional, Tuple

from ..features import ClassLabel, Features, Value
from .base import TaskTemplate


@dataclass
class RelationExtraction(TaskTemplate):
    # `task` is not a ClassVar since we want it to be part of the `asdict` output for JSON serialization
    task_category:str = "relation-extraction"
    task: str = "relation-extraction"
    input_schema: ClassVar[Features] = Features({
        'text': Value('string'),
    })
    # TODO(lewtun): Find a more elegant approach without descriptors.
    label_schema: ClassVar[Features] = Features({
        'subject': Value('string'),
        'object': Value('string'),
        'relation': ClassLabel
    })
    text_column: str = "text"
    subject_column: str = "subject"
    object_column: str = "object",
    relation_column: str = "relation"
    relations: Optional[Tuple[str]] = None

    def __post_init__(self):
        if self.relations:
            if len(self.relations) != len(set(self.relations)):
                raise ValueError("Relation labels must be unique")
            # Cast labels to tuple to allow hashing

            # self.__dict__["labels"] = tuple(sorted(self.labels))
            self.__dict__["relations"] = self.relations


            self.__dict__["label_schema"] = self.label_schema.copy()
            self.label_schema["relation"] = ClassLabel(names=self.relations)

    @property
    def column_mapping(self) -> Dict[str, str]:
        return {
            self.text_column: "text",
            self.subject_column: "subject",
            self.object_column: "object",
            self.relation_column: "relation",
        }
