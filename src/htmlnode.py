class HTMLNode():

    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self) -> str:
        attributes = ""
        if self.props:
            for attribute, value in self.props.items():
                attributes += f' {attribute}="{value}"'
        return attributes
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None) -> None:
        super().__init__(tag, value, None, props)
    
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self) -> str:
        return f'LeafNode({self.tag}, {self.value}, {self.props})'
    