class HTMLNode:
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: list = None,
        props: dict = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props or {}

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        res = ""
        for key, value in self.props.items():
            res += f' {key}="{value}"'
        return res

    def __repr__(self) -> str:
        children_tags = ", ".join(child.tag for child in self.children)
        return f"this is a html node: {self.tag} | {self.value} | {children_tags} | {self.props_to_html()}"


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: list = None,
        props: dict = None,
    ) -> None:
        super().__init__(tag, value, None, props)

    def props_to_html(self):
        if self.tag is None:
            return self.value
        return super().props_to_html()

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props_to_html()})"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: list = None,
        props: dict = None,
    ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")
        
        html = f"<{self.tag}{self.props_to_html()}>"
        
        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"

        return html
