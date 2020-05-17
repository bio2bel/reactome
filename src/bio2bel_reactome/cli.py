# -*- coding: utf-8 -*-

"""CLI for Reactome."""

from .manager import Manager

main = Manager.get_cli()

if __name__ == '__main__':
    main()
