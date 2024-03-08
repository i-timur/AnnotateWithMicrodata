import bs4

from bs4 import BeautifulSoup

class Segmenter:
    def __init__(self, html: str) -> None:
        self.soup = BeautifulSoup(html, 'html.parser')

    def segment_html(self):
        self.__pruning()
        self.__partial_tree_matching()
        self.__backtracking()
        return self.__output()

    def __pruning(self) -> None:
        body = self.soup.find("body")
        body["lid"] = str(-1)
        body["sn"] = str(1)
        self.all_nodes = [body]

        i = 0
        while len(self.all_nodes) > i:
            children = []
            for child in self.all_nodes[i].children:
                if isinstance(child, bs4.element.Tag):
                    children.append(child)
            sn = len(children)

            for child in children:
                child["lid"] = str(i)
                child["sn"] = str(sn)
                self.all_nodes.append(child)
            i += 1

    def __partial_tree_matching(self) -> None:
        self.blocks = []
        lid_old = -2
        i = 0

        while i < len(self.all_nodes):
            node = self.all_nodes[i]

            if 'extracted' in node.attrs:
                i += 1
                continue

            sn, lid = int(node["sn"]), int(node["lid"])

            if lid != lid_old:
                max_window_size = int(sn / 2)
                lid_old = lid

            for window_size in range(1, max_window_size + 1):
                prev_window = []
                current_window = []
                next_window = []

                for window_i in range(i - window_size, i + 2 * window_size):
                    if window_i >= 0 and window_i < len(self.all_nodes) and int(self.all_nodes[window_i]["lid"]) == lid:
                        current_node = self.all_nodes[window_i]

                        if window_i >= i - window_size and window_i < i:
                            prev_window.append(current_node)

                        if window_i >= i and window_i < i + window_size:
                            current_window.append(current_node)

                        if window_i >= i + window_size and window_i < i + 2 * window_size:
                            next_window.append(current_node)

                window_left_equal = self.__compare_nodes(prev_window, current_window)
                window_right_equal = self.__compare_nodes(current_window, next_window)

                if window_left_equal or window_right_equal:
                    self.blocks.append(current_window)
                    i += window_size - 1
                    max_window_size = len(current_window)
                    self.__mark_extracted(current_window)
                    break
            i += 1

    def __mark_extracted(self, nodes) -> None:
        for node in nodes:
            node["extracted"] = ""
            lid = node["lid"]
            parent = node
            while parent.parent is not None:
                parent = parent.parent
                parent["extracted"] = ""
                parent["sid"] = lid

            node_cols = [node]
            for col in node_cols:
                for child in col.children:
                    if isinstance(child, bs4.element.Tag):
                        node_cols.append(child)
                col["extracted"] = ""

    def __compare_nodes(self, nodes1, nodes2):
        if len(nodes1) == 0 or len(nodes2) == 0:
            return False

        return self.__get_nodes_children_structure(nodes1) == self.__get_nodes_children_structure(nodes2)

    def __get_nodes_children_structure(self, nodes):
        structure = ""
        for node in nodes:
            structure += self.__get_node_children_structure(node)
        return structure

    def __get_node_children_structure(self, node):
        nodes = [node]
        structure = ""
        for node in nodes:
            for child in node.children:
                if isinstance(child, bs4.element.Tag):
                    nodes.append(child)
            structure += node.name
        return structure

    def __backtracking(self):
        for node in self.all_nodes:
            if (node.name != "body") and (node.parent is not None) and ("extracted" not in node.attrs) and (
                    "extracted" in node.parent.attrs):
                self.blocks.append([node])
                self.__mark_extracted([node])

    def __get_element(self, node):
        length = 1
        for previous_node in list(node.previous_siblings):
            if isinstance(previous_node, bs4.element.Tag):
                length += 1
        if length > 1:
            return "%s:nth-child(%s)" % (node.name, length)
        else:
            return node.name

    def __get_css_selector(self, node: bs4.element.Tag) -> str:
        path = [self.__get_element(node)]
        for parent in node.parents:
            if parent.name == "[document]":
                break

            path.insert(0, self.__get_element(parent))

        return ' > '.join(path)

    def __output(self):
        segment_ids = []
        record_id = 0
        segments = dict()

        for i, block in enumerate(self.blocks):
            texts = []
            css_selectors = []

            for node in block:
                for text in node.stripped_strings:
                    texts.append(text)

                css_selectors.append(self.__get_css_selector(node))

            if len(texts) == 0:
                continue

            lid = block[0]["lid"]

            if lid not in segment_ids:
                segment_ids.append(lid)

            segment_id = str(segment_ids.index(lid))

            if segment_id not in segments:
                segments[segment_id] = {"segment_id": int(segment_id), "css_selector": self.__get_css_selector(block[0].parent),
                             "records": []}

            segments[segment_id]["records"].append(
                {"record_id": record_id, "texts": texts, "css_selector": css_selectors})
            record_id += 1

        return segments
