class HTMLNode():

    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, HTMLNode):
            return NotImplemented
        
        return(
            self.tag == __value.tag and
            self.value == __value.value and
            self.children == __value.children and
            self.props == __value.props
        )

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

    def to_html(self) -> str:
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self) -> str:
        attributes = ""
        if self.props:
            for attribute, value in self.props.items():
                attributes += f' {attribute}="{value}"'
        return attributes


class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None) -> None:
        super().__init__(tag, value, None, props)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, LeafNode):
            return NotImplemented
        
        return(
            self.tag == __value.tag and
            self.value == __value.value and
            self.props == __value.props
        )
    
    def __repr__(self) -> str:
        return f'LeafNode({self.tag}, {self.value}, {self.props})'
    
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag, None, children, props)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, ParentNode):
            return NotImplemented
        
        return(
            self.tag == __value.tag and
            self.children == __value.children and
            self.props == __value.props
        )

    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")
        if self.children is None:
            raise ValueError("parent node should have children elements")
        
        html = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"

        return html
